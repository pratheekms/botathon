from __future__ import unicode_literals

from django.db import models
import json
# Create your models here.

class UserSteps(models.Model):

	userId = models.CharField(max_length=100, blank=False, null=False)
	userStep = models.IntegerField(default=0, blank=True,null=True)
	context = models.TextField(default=json.dumps({}),blank=True, null=True)

class Genre(models.Model):

	genrename = models.CharField(max_length=200,blank=True, null=True)


	def __unicode__(self):
		return unicode(self.genrename) or u''

class PlotLine(models.Model):

	plotname = models.CharField(max_length=200, blank=True, null=True)

	def __unicode__(self):
		return unicode(self.plotname) or u''


class MovieProperties(models.Model):

	color = models.CharField(max_length=200, blank=False, null=False)
	director_name = models.CharField(max_length=100, blank=False, null=False)
	num_critic_for_reviews = models.IntegerField(default=0)
	duration = models.IntegerField(default=0)
	director_facebook_like = models.IntegerField(default=0)
	actor_3_facebook_likes = models.IntegerField(default=0)
	actor_2_name = models.CharField(max_length=200,blank=True, null=True)
	actor_1_facebook_likes = models.IntegerField(default=0)
	gross = models.IntegerField(default=0)
	genres_ignore = models.CharField(max_length=200,blank=True, null=True)
	actor_1_name = models.CharField(max_length=200,blank=True, null=True)
	movie_title = models.CharField(max_length=200,blank=True, null=True)
	num_voted_users = models.IntegerField(default=0)
	cast_total_facebook_likes = models.IntegerField(default=0)
	actor_3_name = models.CharField(max_length=200,blank=True, null=True)
	facenumber_in_poster = models.IntegerField(default=0)
	plot_keywords_ignore = models.CharField(max_length=200,blank=True, null=True)
	movie_imdb_link = models.CharField(max_length=200,blank=True, null=True)
	num_user_for_reviews = models.IntegerField(default=0)
	language = models.CharField(max_length=200,blank=True, null=True)
	country = models.CharField(max_length=200,blank=True, null=True)
	content_rating = models.CharField(max_length=200,blank=True, null=True)
	budget = models.IntegerField(default=0)
	title_year = models.IntegerField(default=0)
	actor_2_facebook_likes = models.IntegerField(default=0)
	imdb_score = models.FloatField(default=0.0)
	aspect_ratio = models.FloatField(default=0.0)
	movie_facebook_likes = models.IntegerField(default=0)
	genre = models.ManyToManyField(Genre)
	plotline = models.ManyToManyField(PlotLine)

	def __unicode__(self):
		return unicode(self.movie_title) or u''
