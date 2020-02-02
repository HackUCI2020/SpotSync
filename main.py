from flask import Flask, render_template, request
import PlaylistParser.PlaylistParser as PlaylistParser
import PlaylistSyncer.PlaylistDownloader as PlaylistDownloader

app = Flask(__name__)


@app.route('/')
def redirect_from_seed():
    return render_template('form.html')


@app.route('/song-request')
def process_request():
    seed = request.args.get('seed')
    songs = request.args.get('songs')
    num_songs = request.args.get('numSongs')
    content = PlaylistParser.parse(seed, songs, int(num_songs), 'PlaylistParser/')
    return render_template('return-query.html', content=content)


@app.route('/playlist')
def add_playlist():
    return render_template('form-add.html')


@app.route('/add-playlist')
def process_addition():
    ids = request.args.get('ids')
    PlaylistDownloader.download_playlists_from_ids([id.strip() for id in ids.split(',')])


if __name__ == "__main__":
    PlaylistParser.Database.update_databases('PlaylistParser/')
    app.run(debug=False)
