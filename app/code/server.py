import os
import string

from flask import Flask, jsonify, render_template, request, json, session
from flask import flash
from flask import redirect
from flask import send_from_directory

from db import *
import k_anon

app = Flask(__name__)
app.secret_key = 'anonymizationtoolkey'
app.config['UPLOAD_FOLDER'] = '/dataset'
app.config['CONF_FOLDER'] = '/code/arx'
app.config['ori_db_name'] = 'db1'
app.config['ano_db_name'] = 'db2'
ori_dataset_path = None
k_anon_res = None


@app.route('/_array2python')
def array2python():
    session['dataset_attributes'] = json.loads(request.args.get('attributes'))
    attributes = session['dataset_attributes']
    return jsonify(result=attributes)


@app.route('/_categorization2python')
def categorization2python():
    global ori_dataset_path
    if 'attrCategorization' not in request.args:
        flash('No attrCategorization')
        return redirect(request.url)
    # if not session.get('ori_dataset_path', None):
    if not ori_dataset_path:
        flash("Not dataset is set")
        return redirect(request.url)

    conf = json.loads(request.args.get('attrCategorization'))
    conf_path = os.path.join(app.config['CONF_FOLDER'], "conf.json")
    with open(conf_path, 'w') as outfile:
        json.dump(conf, outfile)
    session['conf_path'] = conf_path

    # ori_dataset_path = session.get('ori_dataset_path')
    anon_dataset_path = os.path.join(app.config['UPLOAD_FOLDER'], "anon.csv")

    result_info = k_anon.k_anonymity(ori_dataset_path, conf_path, anon_dataset_path)
    session['anon_dataset_path'] = anon_dataset_path

    print result_info
    global k_anon_res
    k_anon_res = result_info

    mysql = Mysql()
    res = ""
    if ori_dataset_path:
        mysql.create_table(ori_dataset_path, app.config['ori_db_name'])
        mysql.import_csv(ori_dataset_path, app.config['ori_db_name'])
        res += "imported origin dataset"

    if anon_dataset_path:
        mysql.create_table(anon_dataset_path, app.config['ano_db_name'])
        mysql.import_csv(anon_dataset_path, app.config['ano_db_name'])
        res += "imported anon dataset"

    return res


@app.route('/getkanonresult')
def get_k_anon_result():
    global k_anon_res
    if k_anon_res:
        return k_anon_res
    else:
        return "There was an error performing the anonymization. Please check your terminal for more details."


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


@app.route('/results.html')
def resultspage():
    return render_template('results.html')


@app.route('/export.html')
def export():
    return render_template('export.html')


@app.route('/download', methods=['GET'])
def download():
    anon_dataset_path = os.path.join(app.config['UPLOAD_FOLDER'], "anon.csv")
    if os.path.isfile(anon_dataset_path):
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename="anon.csv")
    else:
        return redirect("/export.html")


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

    global ori_dataset_path
    ori_dataset_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

    return "Received the file!"


@app.route('/userQuery', methods=['POST'])
def user_query():
    if 'query' not in request.form:
        flash('No file part')
        return redirect(request.url)

    query = request.form['query']
    mysql = Mysql()
    res = {}
    if "`db`" in query:
        db1_query = string.replace(query, "`db`", "`db1`")
        db2_query = string.replace(query, "`db`", "`db2`")
        res["db1"] = mysql.exec_sql(db1_query)
        res["db2"] = mysql.exec_sql(db2_query)
    elif "`db1`" in query:
        res["db1"] = mysql.exec_sql(query)
    else:
        res["db2"] = mysql.exec_sql(query)

    return json.dumps(res)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
