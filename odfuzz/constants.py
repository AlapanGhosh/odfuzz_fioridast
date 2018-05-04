"""This module contains global constants."""

FUZZER_LOGGER = 'odfuzz'
STATS_LOGGER = 'stats'
FILTER_LOGGER = 'filter'
CONFIG_PATH = 'config/logging/logging.conf'

MONGODB_NAME = 'odfuzz'
MONGODB_COLLECTION = 'entities'

CLIENT = 'sap-client=500'
FORMAT = '$format=json'

ENV_USERNAME = 'SAP_USERNAME'
ENV_PASSWORD = 'SAP_PASSWORD'

EXCLUDE = 'Exclude'
INCLUDE = 'Include'
ORDERBY = 'ORDERBY'
TOP = 'TOP'
SKIP = 'SKIP'
FILTER = 'FILTER'
GLOBAL_ENTITY = '$E_ALL$'
GLOBAL_FUNCTION = '$F_ALL$'

QUERY_OPTIONS = [FILTER, ORDERBY, TOP, SKIP]

STRING_FUNC_PROB = 0.70
MATH_FUNC_PROB = 0.15
DATE_FUNC_PROB = 0.15
FUNCTION_WEIGHT = 0.3
SINGLE_VALUE_PROB = 0.2

LOGICAL_OPERATORS = {'and': 0.5, 'or': 0.5}
BOOLEAN_OPERATORS = {'eq': 0.5, 'ne': 0.5}
EXPRESSION_OPERATORS = {'eq': 0.3, 'ne': 0.3, 'gt': 0.1, 'ge': 0.1, 'lt': 0.1, 'le': 0.1}

SEED_POPULATION = 40
RECURSION_LIMIT = 3
POOL_SIZE = 10
STRING_THRESHOLD = 300
ITERATIONS_THRESHOLD = 1000
SCORE_THRESHOLD = 1000
PARTS_NUM = 2
SCORE_EPS = 200
DEATH_CHANCE = 0.3
ELITE_PROB = 0.7
