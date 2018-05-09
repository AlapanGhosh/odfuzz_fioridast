"""This module contains classes that store and print statistics."""

import os

from datetime import datetime

from odfuzz.mongos import MongoClient
from odfuzz.constants import TOP_ENTITIES, OVERALL_FILE


class Stats(object):
    """A container that holds static data of overall statistics."""

    tests_num = 0
    fails_num = 0
    removed_num = 0
    created_by_mutation = 0
    created_by_crossover = 0
    directory = None
    start_datetime = None


class StatsPrinter(object):
    """A printer that writes all statistics to the defined output."""

    def __init__(self):
        self._mongodb = MongoClient()
        self._stats = Stats()

    def write(self):
        self._write_sorted_entities()
        self._write_overall_stats()

    def _write_sorted_entities(self):
        for entity in self._mongodb.existing_entities():
            file_path = os.path.join(self._stats.directory, 'EntitySet_' + entity + '.txt')
            with open(file_path, 'a', encoding='utf-8') as entity_file:
                for query in self._mongodb.sorted_queries_by_entity(entity, TOP_ENTITIES):
                    info_line = query['http'] + ':' + query['string'] + ':' \
                                              + str(query['score']) + '\n'
                    entity_file.write(info_line)

    def _write_overall_stats(self):
        file_path = os.path.join(self._stats.directory, OVERALL_FILE)
        formatted_output = (
            'Generated tests: ' + str(self._stats.tests_num) + '\n'
            'Failed tests: ' + str(self._stats.fails_num) + '\n'
            'Removed tests: ' + str(self._stats.removed_num) + '\n'
            'Created by mutation: ' + str(self._stats.created_by_mutation) + '\n'
            'Created by crossover: ' + str(self._stats.created_by_crossover) + '\n'
            'Runtime: ' + str(datetime.now() - self._stats.start_datetime) + '\n'
        )
        with open(file_path, 'a', encoding='utf-8') as overall_file:
            overall_file.write(formatted_output)
