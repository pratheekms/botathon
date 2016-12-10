import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movietimeBot.settings')

import django
django.setup()

from movietime.models import MovieProperties, Genre, PlotLine
from django.contrib.auth.models import User
import csv


def populate_movieproperties():


	print "inside populate movieprop"
	with open('movie_metadata.csv', 'r') as f:
		reader =  csv.reader(f, delimiter = '\t', quotechar = '"')
		for i, row in enumerate(reader):

			print i, "th iteration"
			if i == 0:
				continue
			movie_obj = MovieProperties()
			movie_obj.color = row[0]
			movie_obj.director_name = row[1]
			movie_obj.num_critic_for_reviews = row[2]
			movie_obj.duration = row[3]
			movie_obj.director_facebook_like = row[4]
			movie_obj.duration = row[5]
			movie_obj.director_facebook_likes = row[6]
			movie_obj.actor_3_facebook_likes = row[7]
			movie_obj.actor_2_name = row[8]
			movie_obj.actor_1_facebook_likes = row[9]
			movie_obj.gross = row[10]
			movie_obj.genres = row[11]
			movie_obj.actor_1_name = row[12]
			movie_obj.movie_title = row[13]
			movie_obj.num_voted_users = row[14]
			movie_obj.cast_total_facebook_likes = row[15]
			movie_obj.actor_3_name = row[16]
			movie_obj.facenumber_in_poster = row[17]
			movie_obj.plot_keywords = row[18]
			movie_obj.movie_imdb_link = row[19]
			movie_obj.num_user_for_reviews = row[20]
			movie_obj.language = row[21]
			movie_obj.country = row[22]
			movie_obj.content_rating = row[23]
			movie_obj.budget = row[24]
			movie_obj.title_year = row[25]
			movie_obj.actor_2_facebook_likes = row[26]
			movie_obj.imdb_score = row[27]
			movie_obj.aspect_ratio = row[28]
			movie_obj.movie_facebook_likes = row[29]
			movie_obj.save()
			genre_list = [x for x in row[10].split('|')]
			plot_list = [x for x in row[17].split('|')]
			for genre in genre_list:
				genre_obj  = Genre.objects.get(genre_name='%s' % genre)
				movie_obj.genre.add(genre_obj)
			for plot in plot_list:
				plot_obj = PlotLine.objects.get(plot_name='%s' % plot)
				movie_obj.plotline.add(plot_obj)

def populate_genre():

	print "inside populate genre"
	with open('genre.txt', 'r') as f:
		i = 0
		for line in f:
			print i, "th iteration plot"
			genre = Genre()
			genre.genre_name = line.strip()
			genre.save()
			i+=1


def populte_plot():

	print "inside populate plot"
	with open('plot.txt', 'r') as f:
		i=0
		for line in f:
			print i, "th iteration plot"
			plot = PlotLine()
			plot.plot_name = line.strip()
			plot.save()


populate_genre()
populte_plot()
populate_movieproperties()
