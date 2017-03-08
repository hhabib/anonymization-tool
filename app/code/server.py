

from flask import Flask, jsonify, render_template, request, json, session
app = Flask(__name__)
app.secret_key = 'anonymizationtoolkey'
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

if __name__ == '__main__':
    app.run()


