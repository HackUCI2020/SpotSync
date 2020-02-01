from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return "hello world"


if __name__ == "__main__":
    app.run(debug=False)
