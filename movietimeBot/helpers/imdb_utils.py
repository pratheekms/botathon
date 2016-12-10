from collections import defaultdict
import operator
from slugify import slugify

from imdb import IMDb

imdb_obj = IMDb(accessSystem='http')
# imdb_obj = IMDb('sql', uri='mysql://root:admin@35.154.47.219/imdb')

def get_genre_for_movie(movieID):
	movie = imdb_obj.get_movie(movieID) 
	return movie.data['genres']

def get_top_genre_by_id(movieIDs):
	genres_frequency = defaultdict(int)

	for movieID in movieIDs:
		genres = get_genre_for_movie(movieID)
		for genre in genres:
			genres_frequency[genre] += 1

	genres_frequency_list = sorted(genres_frequency.items(), key=operator.itemgetter(1), reverse=True)
	return genres_frequency_list[0]

def get_top_genre_by_name(movie_names):
	genres_frequency = defaultdict(int)

	for movie_name in movie_names:
		movieID, title = get_movieID(movie_name)
		genres = get_genre_for_movie(movieID)
		for genre in genres:
			genres_frequency[genre] += 1

	genres_frequency_list = sorted(genres_frequency.items(), key=operator.itemgetter(1), reverse=True)
	return genres_frequency_list[0]

def get_movieID(name):
	results = imdb_obj.search_movie(name)

	for item in results:
		if item.data['kind'] != 'movie':
			continue
		if slugify(item.data['title']) == slugify(name):
			return item.movieID, item.data['title']


if __name__ == '__main__':
	print get_top_genre_by_name(['john wick', 'the equalizer'])