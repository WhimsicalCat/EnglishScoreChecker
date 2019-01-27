# encoding: utf-8
'''
Created on 2018/10/31

@author: Takimoto Hiroki
'''

from flask import Blueprint, request, current_app, jsonify
import flask
import os
import pickle
from datetime import datetime
import regex
import json
import jsonschema
from werkzeug.exceptions import InternalServerError

non_ascii_pattern = regex.compile('[^\p{ASCII}]')

from scripts import GradeSystem, predict

DEF_blp_name = 'english_score_checker'
blueprint_esc = Blueprint(DEF_blp_name, __name__)

cfp = os.path.dirname(os.path.abspath(__file__)) + os.sep
log_dir = cfp + 'log' + os.sep
if not os.path.isdir(log_dir):
    current_app.logger.info('creating log direcroty: {}'.format(log_dir))
    os.makedirs(log_dir)

with open(current_app.config['API_POST_SCHEMA_PATH']) as infile:
    api_post_schema = json.load(infile)
with open(current_app.config['API_PUT_SCHEMA_PATH']) as infile:
    api_put_schema = json.load(infile)
with open(current_app.config['API_RESULT_SCHEMA_PATH']) as infile:
    api_result_schema = json.load(infile)

class APIError(Exception):
    pass

class NoJSONDataError(APIError):
    pass

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
    grade = predict(inputs)
    output_dict = GradeSystem.output(grade, stats, diff, use_list)
    return output_dict

def remove_non_ascii_chars(src_text):
    removed_text = src_text
    removed_text.replace(u"’", "'")
    removed_text.replace(u'”', '"')
    removed_text.replace(u'“', '"')
    removed_text = non_ascii_pattern.sub('', removed_text)
    return removed_text

@blueprint_esc.route('/api', methods=['POST', 'PUT'])
def api():
    try:
        if not request.is_json:
            raise NoJSONDataError('request is not json data')
        request_json = request.json
        if request.method == 'POST':
            try:
                jsonschema.validate(request_json, api_post_schema)
            except jsonschema.ValidationError as e:
                current_app.logger.exception(e)
                error_responce = {'api_status_code': 601,
                                  'message': 'JSONSchemaError'}
                jsonschema.validate(error_responce, api_result_schema)
                return jsonify(error_responce)
            
            output_dict = get_score(request_json['text'])
            try:
                log_to_pickle(request_json['text'], output_dict)
            except Exception as e:
                current_app.logger.critical(
                    'exception during outputing log to pickle')
                current_app.logger.exception(e)
            sum_of_rate = sum(output_dict['word_diff'])
            g_contents = [item.decode('utf8') 
                          for item 
                          in output_dict['grmitem']]
            result_json = \
                {'cefr_rank': output_dict['grade'],
                 'num_of_sentences': output_dict['stats'][0],
                 'num_of_words': output_dict['stats'][1],
                 'num_of_grammer_contents': len(output_dict['grmitem']),
                 'vocabulary_rates': [{'level': level_name,
                                       'rate': level_rate}
                                      for level_name, level_rate
                                      in zip(['A1', 'A2', 'B1', u'機能語'],
                                             [round(num/sum_of_rate*100, 1) 
                                              for num 
                                              in output_dict['word_diff']])],
                 'used_grammer_contents': [{'grammer_type': gc_name,
                                            'frequency': 1}
                                           for gc_name
                                           in g_contents]}
            if request_json['type'] == 'textbook':
                result_json['num_of_errors'] = 0
            result_responce = {'api_status_code': 200,
                               'message': 'Success',
                               'result': result_json}
            
            try:
                jsonschema.validate(result_responce, api_result_schema)
            except jsonschema.ValidationError as e:
                current_app.logger.exception(e)
                raise

            return jsonify(result_responce)
        elif request.method == 'PUT':
            raise NotImplementedError
    except InternalServerError:
        # this exception was already handled
        pass
    except Exception as e:
        current_app.logger.critical('unhandled exception was raised. '\
                                    'check traceback')
        current_app.logger.exception(e)
        

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
        except Exception as e:
            current_app.logger.critical(
                'exception during outputing log to pickle')
            current_app.logger.exception(e)
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