from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, TextField, validators

import PlaylistParser.PlaylistParser as PlaylistParser

app = Flask(__name__)


class QueryForm(Form):
    seed = TextField('Seed:', validators=[validators.required()])
    songs = TextField('Songs:', validators=[validators.required()])


@app.route('/')
@app.route('/index')
@app.route('/form', methods=["GET", "POST"])
def redirect_from_seed():
    form = QueryForm(request.form)
    if request.method == 'POST':
        seed = request.form['seed']
        songs = request.form['songs']
        return render_template('return-query.html', content=PlaylistParser.parse(seed, songs))
    else:
        return render_template('form.html', form=form)


def results_from_seed(songs):
    return render_template('return-query.html', content=songs)


if __name__ == "__main__":
    app.run(debug=False)
