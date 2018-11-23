# encoding: utf-8
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
    return output_dict


@blueprint_esc.route('/')
def index():
    input_text = request.args.get('txt')
    if input_text:
        output_dict = get_score(input_text)
        sum_of_rate = sum(output_dict['word_diff'])
        chart_datas = [{'data': [round(num/sum_of_rate*100, 1) 
                                 for num 
                                 in output_dict['word_diff']],
                        'backgroundColor': [
                            'rgba(255, 0, 0, 0.2)',
                            'rgba(0, 255, 0, 0.2)',
                            'rgba(0, 0, 255, 0.2)',
                            'rgba(255, 255, 0, 0.2)',],}]
        chart_labels = ['A1', 'A2', 'B1', u'機能語']
        chart_data = {'datasets': chart_datas,
                      'labels': chart_labels}
        chart_options = {'cutoutPercentage': 0}
        ret_json = {'chart_data': chart_data,
                    'chart_options': chart_options,
                    'num_of_chars': output_dict['stats'][0],
                    'num_of_words': output_dict['stats'][1],
                    'num_of_incorrect': 0,
                    'num_of_used_grammer_content': len(output_dict['grmitem']),
                    'CEFR_level': output_dict['grade']}
        g_contents = [item.decode('utf8') for item in output_dict['grmitem']]
        return flask.render_template(
            'checker_page.html',
            data=ret_json,
            grammer_contents=g_contents,
            is_essay=True if request.args.get('type') == '#essay' else False)
    else:
        return flask.render_template('checker_page.html')

@blueprint_esc.route('/count_word', methods=['POST'])
def count_num_of_words():
    text_data = flask.request.form['data']
    return '{}'.format(len(text_data.strip('.').split()))