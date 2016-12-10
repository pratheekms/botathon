from __future__ import unicode_literals

from django.db import models

# Create your models here.

class UserSteps(models.Model):

	userId = models.CharField(max_length=100, blank=False, null=False)
	userStep = models.IntegerField(default=0, blank=True,null=True)


class Genre(models.Model):

	genre_name = models.CharField(max_length=200,blank=True, null=True)
	

	def __unicode__(self):
		return unicode(self.genre_name) or u''


class PlotLine(models.Model):

	plot_name = models.CharField(max_length=200, blank=True, null=True)
	
	def __unicode__(self):
		return unicode(self.plot_name) or u''



class MovieProperties(models.Model):

	color = models.CharField(max_length=200, blank=False, null=False)
	director_name = models.CharField(max_length=100, blank=False, null=False)
	num_critic_for_reviews = models.IntegerField()
	duration = models.IntegerField()
	director_facebook_like = models.IntegerField()
	duration = models.IntegerField()
	director_facebook_likes = models.IntegerField()
	actor_3_facebook_likes = models.IntegerField()
	actor_2_name = models.IntegerField()
	actor_1_facebook_likes = models.IntegerField()
	gross = models.IntegerField()
	genres = models.CharField(max_length=200,blank=True, null=True)
	actor_1_name = models.CharField(max_length=200,blank=True, null=True)
	movie_title = models.CharField(max_length=200,blank=True, null=True)
	num_voted_users = models.IntegerField()
	cast_total_facebook_likes = models.IntegerField()
	actor_3_name = models.CharField(max_length=200,blank=True, null=True)
	facenumber_in_poster = models.IntegerField()
	plot_keywords = models.CharField(max_length=200,blank=True, null=True)
	movie_imdb_link = models.CharField(max_length=200,blank=True, null=True)
	num_user_for_reviews = models.IntegerField()
	language = models.CharField(max_length=200,blank=True, null=True)
	country = models.CharField(max_length=200,blank=True, null=True)
	content_rating = models.CharField(max_length=200,blank=True, null=True)
	budget = models.IntegerField()
	title_year = models.IntegerField()
	actor_2_facebook_likes = models.IntegerField()
	imdb_score = models.IntegerField()
	aspect_ratio = models.IntegerField()
	movie_facebook_likes = models.IntegerField()
	genre = models.ManyToManyField(Genre)
	plotline = models.ManyToManyField(PlotLine)

	def __unicode__(self):
		return unicode(self.movie_title) or u''




















