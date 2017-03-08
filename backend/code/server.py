from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/api/')
def hello():
    return 'Hello World!\n'

@app.route('/_array2python')
def array2python():
    attributelist = request.args.get('attributes', [])
    return jsonify(result=attributeist)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
