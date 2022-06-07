'''
Created on 2018/03/28

@author: Takimoto Hiroki
'''

import os

cfp = os.path.dirname(os.path.abspath(__file__)) + os.sep
schema_root = cfp + 'EnglishScoreChecker{sep}static'\
                    '{sep}schema{sep}'.format(sep=os.sep)

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    API_POST_SCHEMA_PATH \
        = '{root}get_score_schema.json'.format(root=schema_root)
    API_PUT_SCHEMA_PATH \
        = '{root}put_score_schema.json'.format(root=schema_root)
    API_RESULT_SCHEMA_PATH \
        = '{root}result_schema.json'.format(root=schema_root)

class DevelopConfig(BaseConfig):
    DEBUG = True
    TESTING = True

class ProductionConfig(BaseConfig):
    pass
