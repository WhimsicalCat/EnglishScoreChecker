'''
Created on 2018/10/31

@author: Takimoto Hiroki
'''

from flask import Blueprint
import flask

DEF_blp_name = 'english_score_checker'
blueprint_esc = Blueprint(DEF_blp_name, __name__)

@blueprint_esc.route('/')
def index():
    return flask.render_template('checker_page.html')

