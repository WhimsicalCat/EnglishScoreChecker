'''
Created on 2018/10/31

@author: Takimoto Hiroki
'''

from flask import Blueprint, request
import flask

DEF_blp_name = 'english_score_checker'
blueprint_esc = Blueprint(DEF_blp_name, __name__)

@blueprint_esc.route('/')
def index():
    input_text = request.args.get('txt')
    if input_text:
        ret_json = {'chart_data':'hogehoge',
                    'num_of_chars': 10,
                    'num_of_words': 10,
                    'num_of_incorrect': 1,
                    'num_of_used_grammer_content': 3}
        return flask.render_template(
            'checker_page.html',
            data=ret_json)
    else:
        return flask.render_template('checker_page.html')

@blueprint_esc.route('/count_word', methods=['POST'])
def count_num_of_words():
    text_data = flask.request.form['data']
    return '{}'.format(len(text_data.strip('.').split()))