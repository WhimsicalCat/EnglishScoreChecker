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
        chart_datas = [{'data': [10, 20, 30],
                        'backgroundColor': [
                            'rgba(255, 0, 0, 0.2)',
                            'rgba(0, 255, 0, 0.2)',
                            'rgba(0, 0, 255, 0.2)',],}]
        chart_labels = ['red', 'green', 'blue']
        chart_data = {'datasets': chart_datas,
                      'labels': chart_labels}
        chart_options = {'cutoutPercentage': 0}
        ret_json = {'chart_data': chart_data,
                    'chart_options': chart_options,
                    'num_of_chars': 10,
                    'num_of_words': 10,
                    'num_of_incorrect': 1,
                    'num_of_used_grammer_content': 3}
        g_contents = ['grammer like something1',
                      'grammer like something2',
                      'grammer like something3']
        return flask.render_template(
            'checker_page.html',
            data=ret_json,
            grammer_contents=g_contents)
    else:
        return flask.render_template('checker_page.html')

@blueprint_esc.route('/count_word', methods=['POST'])
def count_num_of_words():
    text_data = flask.request.form['data']
    return '{}'.format(len(text_data.strip('.').split()))