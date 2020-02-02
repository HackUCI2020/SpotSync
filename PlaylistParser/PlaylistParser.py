import pickle
import pathlib


def parse(seed, songs, num_songs):
    db = Database()
    seed = seed.split(',')
    songs = songs.split(',')
    print(seed)
    print(songs)
    print(num_songs)
    return db.get_matching_songs(songs, seed, num_songs)


def get_untracked_files(directory: pathlib.Path, db: {str:{str}}):
    for file_path in pathlib.Path(directory).iterdir():
        if file_path.name not in db.keys():
            yield file_path


class Database:
    DATABASE_PICKLE_LINK = "db.pickle"
    PLAYLIST_TEXTS_DIRECTORY = "playlists/"

    def __init__(self, relative_path=""):
        self._db: {str:{str}} = {}
        self.load(relative_path)
        print(self._db)

    @staticmethod
    def update_databases(relative_path=""):
        db = Database(relative_path)
        db.parse_files(relative_path)
        db.save(relative_path)

    def load(self, relative_path=""):
        with open(relative_path+Database.DATABASE_PICKLE_LINK, 'rb') as pickledDB:
            self._db = pickle.load(pickledDB)

    def clear(self):
        self._db = {}

    def save(self, relative_path=""):
        with open(relative_path+Database.DATABASE_PICKLE_LINK, 'wb') as pickledDB:
            pickle.dump(self._db, pickledDB)

    def parse_files(self, relative_path=""):
        for file in get_untracked_files(pathlib.PurePath(relative_path+Database.PLAYLIST_TEXTS_DIRECTORY), self._db):
            self._db[file.name] = set()
            with open(str(file), 'r') as playlist:
                for line in playlist:
                    self._db[file.name].add(line.strip())
        self.save()

    def get_all_songs(self):
        return set.union(*[songs for songs in self._db.values()])

    def get_matching_songs(self, seeds, song_list, num_songs):
        song_dict = dict()
        for song in song_list:
            song_dict[song] = self.get_compatibility(song, seeds)
        songs = sorted(song_dict.items(), key=lambda x: x[1], reverse=True)
        return [song_score_match[0] for song_score_match in songs[0:num_songs]]

    # returns how often the song occurs with seeds
    def get_compatibility(self, song, seeds) -> float:
        compatibilities = [self.get_compatibility_with_seed(song, seed) for seed in seeds]
        return sum(compatibilities)/len(compatibilities)

    def get_compatibility_with_seed(self, song, seed) -> float:
        compatibilities = [int(song in songs and seed in songs) for playlist, songs in self._db.items()]
        weight = sum(compatibilities)/len(compatibilities)
        return sum(compatibilities)/len(compatibilities)

    def detect_compatibility(self, seeds: [str]):
        def match_playlist(seeds: [str], songs: {str}):
            count = 0
            for seed in seeds:
                if seed in songs:
                    count += 1
            return count / len(seeds)
        compatibility = [match_playlist(seeds, songs) for playlist, songs in self._db.items()]
        return sum(compatibility)/len(compatibility)


if __name__ == "__main__":
    db = Database()
    db.parse_files()
    print( db.get_matching_songs(db.get_all_songs(),
                          10,
                          ['song 1', 'song 2']))