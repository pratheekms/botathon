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
		reader =  csv.reader(f, delimiter = ',', quotechar = '"')
		for i, row in enumerate(reader):

			print i, "th iteration"
			# print row, len(row)
			if i == 0:
				continue
			movie_obj = MovieProperties()
			movie_obj.color = row[0]
			movie_obj.director_name = row[1]
			try:
				movie_obj.num_critic_for_reviews = int(row[2])
			except:
				pass
			try:
				movie_obj.duration = int(row[3])
			except:
				pass
			try:
				movie_obj.director_facebook_like = int(row[4])
			except:
				pass
			try:
				movie_obj.actor_3_facebook_likes = int(row[5])
			except:
				pass
			movie_obj.actor_2_name = row[6]
			try:
				movie_obj.actor_1_facebook_likes = int(row[7])
			except:
				pass
			try:
				movie_obj.gross = int(row[8])
			except:
				pass
			movie_obj.genres_ignore = row[9]
			movie_obj.actor_1_name = row[10]
			movie_obj.movie_title = row[11]
			try:
				movie_obj.num_voted_users = int(row[12])
			except:
				pass
			try:
				movie_obj.cast_total_facebook_likes = int(row[13])
			except:
				pass
			movie_obj.actor_3_name = row[14]
			try:
				movie_obj.facenumber_in_poster = int(row[15])
			except:
				pass
			movie_obj.plot_keywords_ignore = row[16]
			movie_obj.movie_imdb_link = row[17]
			try:
				movie_obj.num_user_for_reviews = int(row[18])
			except:
				pass
			movie_obj.language = row[19]
			movie_obj.country = row[20]
			movie_obj.content_rating = row[21]
			try:
				movie_obj.budget = int(row[22])
			except:
				pass
			try:
				movie_obj.title_year = int(row[23])
			except:
				pass
			try:
				movie_obj.actor_2_facebook_likes = int(row[24])
			except:
				pass
			try:
				movie_obj.imdb_score = float(row[25])
			except:
				pass
			try:
				movie_obj.aspect_ratio = float(row[26])
			except:
				pass
			try:
				movie_obj.movie_facebook_likes = int(row[27])
			except:
				pass
			movie_obj.save()
			genre_list = [x for x in row[9].split('|')]
			plot_list = [x for x in row[16].split('|')]
			# print genre_list, plot_list
			for genre in genre_list:
				# print genre
				genre_obj, created  = Genre.objects.get_or_create(genrename=genre)
				movie_obj.genre.add(genre_obj)
			for plot in plot_list:
				# print plot
				try:
					plot_obj, created = PlotLine.objects.get_or_create(plotname=plot)
					movie_obj.plotline.add(plot_obj)
				except:
					print plot
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
			i += 1

# populate_genre()
# populte_plot()
populate_movieproperties()
