import os

from flask import Flask, jsonify, render_template, request, json, session
from flask import flash
from flask import redirect

app = Flask(__name__)
app.secret_key = 'anonymizationtoolkey'
app.config['UPLOAD_FOLDER'] = '/dataset'
# dataset_attributes = []
 
@app.route('/_array2python')
def array2python():
   session['dataset_attributes'] = json.loads(request.args.get('attributes'))
   attributes = session['dataset_attributes']
   return jsonify(result=attributes)

@app.route('/_python2array')
def python2array():
	attributes = session.get('dataset_attributes', None)
	print attributes
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

@app.route('/postcsv', methods = ['POST'])
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
    return "Received the file!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)


