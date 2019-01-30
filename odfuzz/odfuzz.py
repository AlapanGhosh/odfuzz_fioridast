from gevent import monkey

monkey.patch_all()

import sys
import signal
import logging
import gevent

from datetime import datetime
from functools import partial

from odfuzz.arguments import ArgParser
from odfuzz.fuzzer import Manager
from odfuzz.statistics import Stats, StatsPrinter
from odfuzz.loggers import init_loggers, DirectoriesCreator
from odfuzz.scatter import ScatterPlotter
from odfuzz.mongos import CollectionCreator
from odfuzz.constants import INFINITY_TIMEOUT
from odfuzz.exceptions import ArgParserError, ODfuzzException


def main():
    execute(sys.argv[1:])


def execute(arguments, bind=None):
    arg_parser = ArgParser()
    try:
        parsed_arguments = arg_parser.parse(arguments)
    except ArgParserError as argparser_error:
        sys.exit(argparser_error)

    init_logging(parsed_arguments)

    collection_name = create_collection_name(parsed_arguments)
    set_signal_handler(collection_name, parsed_arguments.plot)

    # Argument 'bind' is used for binding the self instance of another process, e.g. celery
    run_fuzzer(bind, parsed_arguments, collection_name)


def init_logging(arguments):
    directories_creator = DirectoriesCreator(arguments.logs, arguments.stats)
    directories = directories_creator.create()
    init_basic_stats(directories.stats)
    init_loggers(directories.logs, directories.stats)


def init_basic_stats(stats_directory):
    Stats.directory = stats_directory
    Stats.start_datetime = datetime.now()


def create_collection_name(parsed_arguments):
    service_parts = parsed_arguments.service.rstrip('/').rsplit('/', 1)
    if len(service_parts) == 1:
        service_name = service_parts[0]
    else:
        service_name = service_parts[1]
    collection_creator = CollectionCreator(service_name)
    collection_name = collection_creator.create()
    return collection_name


def set_signal_handler(db_collection_name, plot_graph):
    gevent.signal(signal.SIGINT, partial(signal_handler, db_collection_name, plot_graph))


def run_fuzzer(bind, parsed_arguments, collection_name):
    manager = Manager(bind, parsed_arguments, collection_name)
    try:
        if parsed_arguments.timeout == INFINITY_TIMEOUT:
            manager.start()
        else:
            gevent.with_timeout(parsed_arguments.timeout, manager.start)
    except ODfuzzException as ex:
        sys.stderr.write(str(ex))
        sys.exit(1)
    except gevent.Timeout:
        signal_handler(collection_name, parsed_arguments.plot)


def signal_handler(db_collection_name, plot_graph):
    exit_message = 'Program interrupted. Exiting...'
    logging.info(exit_message)
    sys.stdout.write('\n' + exit_message + '\n')

    stats = StatsPrinter(db_collection_name)
    stats.write()

    if plot_graph:
        scatter = ScatterPlotter(Stats.directory)
        scatter.create_plot()

    sys.exit(0)

if __name__ == '__main__':
    main()