import os

from flask import Flask, jsonify, render_template, request, json, session
from flask import flash
from flask import redirect
from db import *
import k_anon

app = Flask(__name__)
app.secret_key = 'anonymizationtoolkey'
# app.config['UPLOAD_FOLDER'] = '/Users/Billdqu/drive/classes/08605EPS/prj/at/anonymization-tool/dataset'
app.config['UPLOAD_FOLDER'] = '/dataset'
# app.config['CONF_FOLDER'] = '/Users/Billdqu/drive/classes/08605EPS/prj/at/anonymization-tool/app/code/arx'
app.config['CONF_FOLDER'] = '/code/arx'
app.config['ori_db_name'] = 'db1'
app.config['ano_db_name'] = 'db2'


@app.route('/_array2python')
def array2python():
    session['dataset_attributes'] = json.loads(request.args.get('attributes'))
    attributes = session['dataset_attributes']
    return jsonify(result=attributes)

@app.route('/_categorization2python')
def categorization2python():
    session['attributes_categorization'] = json.loads(request.args.get('attrCategorization'))
    attrCategorization = session['attributes_categorization']
    return jsonify(result=attrCategorization)


@app.route('/_python2array')
def python2array():
    attributes = session.get('dataset_attributes', None)
    # print attributes
    return jsonify(result=attributes)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/import.html')
def importpage():
    return render_template('import.html')


@app.route('/anonymize.html')
def suppression():
    return render_template('anonymize.html')


@app.route('/postcsv', methods=['POST'])
def get_post_csv():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    session['ori_dataset_path'] = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

    return "Received the file!"

@app.route('/kanon', methods=['POST'])
def k_anonymity():
    if 'k' not in request.form:
        flash('No K')
        return redirect(request.url)
    if 'conf' not in request.files:
        flash('No Conf Json File')
        return redirect(request.url)

    if not session.get('ori_dataset_path', None):
        flash("Not dataset is set")
        return redirect(request.url)

    conf = request.files['conf']

    if conf.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if conf:
        conf.save(os.path.join(app.config['CONF_FOLDER'], conf.filename))


    ori_dataset_path = session.get('ori_dataset_path')
    k = request.form['k']
    conf_json_path = os.path.join(app.config['CONF_FOLDER'], conf.filename)
    anon_dataset_path = os.path.join(app.config['UPLOAD_FOLDER'], "anon.csv")

    k_anon.k_anonymity(ori_dataset_path, k, conf_json_path, anon_dataset_path)
    session['anon_dataset_path'] = anon_dataset_path

    return ""

@app.route('/import2db')
def import2db():
    mysql = Mysql()
    res = ""
    if session.get('ori_dataset_path', None):
        mysql.create_table(session.get('ori_dataset_path', None), app.config['ori_db_name'])
        mysql.import_csv(session.get('ori_dataset_path', None), app.config['ori_db_name'])
        res += "imported origin dataset"

    if session.get('anon_dataset_path', None):
        mysql.create_table(session.get('anon_dataset_path', None), app.config['ano_db_name'])
        mysql.import_csv(session.get('anon_dataset_path', None), app.config['ano_db_name'])
        res += "imported anon dataset"

    return res


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
