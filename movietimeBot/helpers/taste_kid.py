from urllib2 import Request, urlopen, URLError
import re

string = []

def get_tastekid_movie(movies):
    for movie in movies:
        rep_spa = re.sub(' ','+',movie)
        clean_str = re.sub('&','and',rep_spa)
        string.append(clean_str)
        string.append('%2C+')
    movie_list = ''.join(string)
    movie_list = movie_list[:-4]

    # string = 'need+for+speed%2C+fast+and+furious'
    # headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
    req = Request('http://www.tastekid.com/api/similar?q='+movie_list+'&type=movies&k=107997-moviebot-IQH0CM4W')

    response = urlopen(req)
    rec_movies = response.read()
    print rec_movies
    return rec_movies

if __name__ == "__main__":
	get_tastekid_movie()
