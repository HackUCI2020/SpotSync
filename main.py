from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, TextField, validators

import PlaylistParser.PlaylistParser as PlaylistParser

app = Flask(__name__)


class QueryForm(Form):
    seed = TextField('Seed:', validators=[validators.required()])
    songs = TextField('Songs:', validators=[validators.required()])


@app.route('/')
def redirect_from_seed():
    return render_template('form.html')


@app.route('/song-request')
def process_request():
    seed = request.args.get('seed')
    songs = request.args.get('songs')
    return render_template('return-query.html', content=PlaylistParser.parse(seed, songs, 5))


if __name__ == "__main__":
    PlaylistParser.Database.update_databases('PlaylistParser/')
    app.run(debug=False)
