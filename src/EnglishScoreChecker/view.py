# encoding: utf-8
'''
Created on 2018/10/31

@author: Takimoto Hiroki
'''

from flask import Blueprint, request, current_app
import flask
import os
import pickle
from datetime import datetime
import regex

non_ascii_pattern = regex.compile('[^\p{ASCII}]')

from scripts import GradeSystem, clf

DEF_blp_name = 'english_score_checker'
blueprint_esc = Blueprint(DEF_blp_name, __name__)

cfp = os.path.dirname(os.path.abspath(__file__)) + os.sep
log_dir = cfp + 'log' + os.sep
if not os.path.isdir(log_dir):
    current_app.logger.info('creating log direcroty: {}'.format(log_dir))
    os.makedirs(log_dir)

def log_to_pickle(input_text, output_dict):
    timestamp = datetime.now()
    dict_to_pickle = {'input': input_text,
                      'output': output_dict,
                      'time': timestamp.strftime("%Y/%m/%d %H:%M:%S")}
    filename = timestamp.strftime('%Y%m%d_%H%M%S')
    filepath ='{dir}{name}.pkl'.format(dir = log_dir,
                                       name=filename)
    with open(filepath, mode='wb') as outfile:
        pickle.dump(dict_to_pickle, outfile, protocol=2)
    current_app.logger.info('output log to {}'.format(filepath))

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

def remove_non_ascii_chars(src_text):
    removed_text = src_text
    removed_text.replace(u"’", "'")
    removed_text.replace(u'”', '"')
    removed_text.replace(u'“', '"')
    removed_text = non_ascii_pattern.sub('', removed_text)
    return removed_text

@blueprint_esc.route('/')
def index():
    input_text = request.args.get('txt')
    if input_text:
        if non_ascii_pattern.search(input_text):
            flask.flash(u'非ASCII文字の入力は現在対応中です。非ASCII文字を無視してスコアを計算しました。')
            input_text = remove_non_ascii_chars(input_text)
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
        try:
            log_to_pickle(input_text, output_dict)
        except:
            current_app.logger.exception(
                'exception during outputing log to pickle')
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