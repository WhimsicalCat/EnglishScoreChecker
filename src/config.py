'''
Created on 2018/03/28

@author: Takimoto Hiroki
'''

import os

class BaseConfig(object):
    DEBUG = False
    TESTING = False

class DevelopConfig(BaseConfig):
    DEBUG = True
    TESTING = True

class ProductionConfig(BaseConfig):
    pass