import os

from flask import Flask, jsonify, render_template, request, json, session
from flask import flash
from flask import redirect
from db import *

app = Flask(__name__)
app.secret_key = 'anonymizationtoolkey'
app.config['UPLOAD_FOLDER'] = '/dataset'
app.config['ori_db_name'] = 'db1'
app.config['ano_db_name'] = 'db2'


@app.route('/_array2python')
def array2python():
    session['dataset_attributes'] = json.loads(request.args.get('attributes'))
    attributes = session['dataset_attributes']
    return jsonify(result=attributes)

@app.route('/_suppression2python')
def suppression2python():
    session['suppression_attributes'] = json.loads(request.args.get('suppressedAttr'))
    suppressedAttr = session['suppression_attributes']
    index2suppress()
    return jsonify(result=suppressedAttr)

# Returns a python dictionary, suppress{column number of attribute: number of characters to suppress}. Value of number of characters to suppress is either "all" or a number
@app.route('/_index2suppress')
def index2suppress():
    suppressedAttr = session.get('suppression_attributes', None)
    attributes = session.get('dataset_attributes', None)
    i = len(suppressedAttr)
    j = 1
    suppress = {}
    
    for key in suppressedAttr:
        colNum = attributes.index(key)
        value = suppressedAttr[key]
        suppress[colNum] = value
    # print suppress
    return suppress
        


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


@app.route('/suppression.html')
def suppression():
    return render_template('suppression.html')


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


@app.route('/import2db')
def import2db():
    mysql = Mysql()
    res = ""
    if session.get('ori_dataset_path', None):
        mysql.create_table(session.get('ori_dataset_path', None), app.config['ori_db_name'])
        mysql.import_csv(session.get('ori_dataset_path', None), app.config['ori_db_name'])
        res += "imported origin dataset"

    if session.get('ano_dataset_path', None):
        mysql.create_table(session.get('ano_dataset_path', None), app.config['ano_db_name'])
        mysql.import_csv(session.get('ano_dataset_path', None), app.config['ano_db_name'])
        res += "imported anon dataset"

    return res


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
