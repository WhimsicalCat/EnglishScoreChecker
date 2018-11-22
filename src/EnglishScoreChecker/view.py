'''
Created on 2018/10/31

@author: Takimoto Hiroki
'''

from flask import Blueprint, request
import flask

from scripts import GradeSystem, clf

DEF_blp_name = 'english_score_checker'
blueprint_esc = Blueprint(DEF_blp_name, __name__)

def get_score(input_text):
    data = input_text + ' '
    surface = GradeSystem.Surface(unicode(data))
    ngram, stats, diff = surface.features()
    grmitem = GradeSystem.GrmItem(unicode(data))
    grm, pos_ngram, use_list = grmitem.features()
    inputs = GradeSystem.Feature(ngram=ngram, 
                                 pos_ngram=pos_ngram, 
                                 grmitem=grm, 
                                 word_difficulty=diff, 
                                 stats=stats).concat()
    grade = clf.predict(inputs)
    output_dict = GradeSystem.output(grade, stats, diff, use_list)
    print(output_dict)
    return output_dict


@blueprint_esc.route('/')
def index():
    input_text = request.args.get('txt')
    if input_text:
        output_dict = get_score(input_text)
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