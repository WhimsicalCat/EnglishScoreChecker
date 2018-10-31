'''
Created on 2018/10/29

@author: Takimoto Hiroki
'''

from flask import Flask

def create_app(config_object='config.BaseConfig'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    from .view import blueprint_esc
    app.register_blueprint(blueprint_esc)
    
    return app

app = create_app()