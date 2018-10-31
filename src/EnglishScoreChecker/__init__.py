'''
Created on 2018/10/29

@author: Takimoto Hiroki
'''

from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from .view import blueprint_esc
    app.register_blueprint(blueprint_esc)
    
    return app

app = create_app()