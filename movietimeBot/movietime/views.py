from django.conf import settings
from django.shortcuts import render
from django.views import generic
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from models import UserSteps
from pymessenger.bot import Bot

# Create your views here.

import logic
from slugify import slugify
import json
from multiprocessing import Process

from HotstarScrape import myScraper as hotstar_scrape
from NetflixScrape import myScraper as netflix_scrape
from PVRScrape import myScraper as pvr_scrape
import taste_kid

class MovieTimeBot(generic.View):

	access_token = settings.ACCESS_TOKEN
	bot = Bot(access_token)

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)


	def get(self, request, *args, **kwargs):
		"""get request to handle input from the facebook bot"""
		if self.request.GET['hub.verify_token'] == '42873292':
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error, invalid token')


	def send_message(self,message, fb_id):

		post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % self.access_token 
		response_msg = json.dumps(message)
		status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)




	def post(self, request, *args, **kwargs):

		incoming_message = json.loads(self.request.body.decode('utf-8'))
		print incoming_message['entry'],"**********************"
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				if 'message' in message:
					print message, "message"
					print message['sender']['id']
					# step 1 replying with a user
					fb_id = message['sender']['id']
					usersteps_obj, Create = UserSteps.objects.get_or_create(userId=fb_id)
					if message['message']['text'].lower() in ['hey','hi','hello','hola']:
						print "check"
						message = {"recipient":{"id":fb_id},"message":{"text":"Who is yer favorite pirate yee hhharr? I am MoViEPiRaTe!! Here to help you find a good movie \n I will find the best movie for you.","quick_replies":[{"content_type":"text","title":"Actor","payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"},{"content_type":"text","title":"Genre","payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"},]}}
						self.send_message(message,fb_id)
						user_obj, Create = UserSteps.objects.get_or_create(userId=fb_id)
						user_obj.userStep = 1
						user_obj.context = json.dumps({})
						user_obj.save()
					# if message['message']['text'] == "something else":
					# 	user_obj, Create = UserSteps.objects.get_or_create(userId=fb_id)
					# 	context = json.loads(user_obj.context)


					elif message['message']['text'] == 'Actor':
						print "Actor"
						# message = {"recipient":{"id":fb_id},"message":{"text":"Actor"}}
						# self.send_message(message,fb_id)

					# 	# some function of pratheeks
						user_obj, Create = UserSteps.objects.get_or_create(userId=fb_id)
						user_obj.userStep = 2
						user_obj.save()

						actor_suggestion = logic.actor_suggestion()
						message = {"recipient":{"id":fb_id},"message":{"text":"May be you will like some of these actors","quick_replies":[]}}
						for actor in actor_suggestion:
							print actor
							message["message"]["quick_replies"].append({"content_type":"text","title":actor,"payload":actor})

						# message["message"]["quick_replies"].append({"content_type":"text","title":"something else","payload":"something else"})
						print message
						context = json.loads(user_obj.context)
						context['actors'] = actor_suggestion
						print context
						user_obj.context  = json.dumps(context)
						user_obj.save()
						self.send_message(message,fb_id)
						


					elif message['message']['text'] == 'Genre':
						print 'Genre'
						# some functions of pratheeks
						user_obj, Create = UserSteps.objects.get_or_create(userId=fb_id)
						user_obj.userStep = 2
						user_obj.save()

						genre_suggestion = logic.genre_suggestion()
						message = {"recipient":{"id":fb_id},"message":{"text":"May be you will like some of these genres","quick_replies":[]}}
						for genre in genre_suggestion:
							print genre
							message["message"]["quick_replies"].append({"content_type":"text","title":genre,"payload":genre})

						# message["message"]["quick_replies"].append({"content_type":"text","title":"something else","payload":"something else"})
						print message
						context = json.loads(user_obj.context)
						context['genres'] = genre_suggestion
						print context
						user_obj.context  = json.dumps(context)
						user_obj.save()
						self.send_message(message,fb_id)


					else:
						user_obj, Create = UserSteps.objects.get_or_create(userId=fb_id)
						context = json.loads(user_obj.context)
						input_text = message['message']['text']
						input_payload = message['message']['quick_reply']['payload']
						print input_text, input_payload
						print context
						print 'movies' in context
						# print input_text in context['movies']
						if 'movies' in context and input_payload in context['movies']:
							print "movie selection made"
							# user_obj, Create = UserSteps.objects.get_or_create(userId=fb_id)
							context['movies'] = [input_text]
							user_obj.userStep = 4
							user_obj.context  = json.dumps(context)
							user_obj.save()	
							
							# self.send_message({"recipient":{"id":fb_id},"sender_action":"typing_on"}, fb_id)
							# hotstar = hotstar_scrape(input_payload)
							# hotstar_status = hotstar.scrape()
							hotstar_status = 'Available'
							# netflix = netflix_scrape(input_payload)
							# netflix_status = netflix.scrape()
							netflix_status = 'Not Available'
							# pvr = pvr_scrape(input_payload)
							# pvr_status = pvr.scrape()
							pvr_status = 'Not Available'
							more_movies = taste_kid.get_tastekid_movie([input_payload,])
							print more_movies
							import time
							message = {"recipient":{"id":fb_id},"message":{"text":"PVR : "+pvr_status,}}
							self.send_message(message,fb_id)
							time.sleep(3)
							message = {"recipient":{"id":fb_id},"message":{"text":"Netflix : "+netflix_status,}}
							self.send_message(message,fb_id)
							time.sleep(6)

							message = {"recipient":{"id":fb_id},"message":{"text":"Hotstar : "+hotstar_status,}}
							self.send_message(message,fb_id)
							time.sleep(4)

							# self.send_message({"recipient":{"id":fb_id},"sender_action":"typing_on"},fb_id)
							message = {"recipient":{"id":fb_id},"message":{"text":"I feel You would like these ones as well","quick_replies":[]}}

							for movie in more_movies:
								print movie
								message["message"]["quick_replies"].append({"content_type":"text","title":movie,"payload":movie})

							# message["message"]["quick_replies"].append({"content_type":"text","title":"something else","payload":"something else"})

							self.send_message(message,fb_id)
							
							message = {
										 "recipient":{
										   "id":fb_id
										 },
										 "message":{
										   "attachment":{
										     "type":"image",
										     "payload":{
										       "url":"https://i.ytimg.com/vi/dnu1TxoyrVY/maxresdefault.jpg"
										     }
										   }
										 }
										}
							self.send_message(message,fb_id)
							message = {"recipient":{"id":fb_id},"message":{"text":"See ya on the high tide ol buddy. Ba bye. Have fun"}}
							self.send_message(message,fb_id)
							user_obj.context = json.dumps({'done':'done'})
							user_obj.save()
							import sys
							sys.exit()
						elif 'actors' in context and input_text in context['actors']:

							message = {"recipient":{"id":fb_id},"message":{"text":"Almost there and Keep trying I promise you will hit your next dream movie!","quick_replies":[]}}
							#check if actor suggestion
							user_obj, Create = UserSteps.objects.get_or_create(userId=fb_id)
							movie_suggestion = []
							movie_suggestion = logic.movie_suggestion_by_actor(input_text)

							context['movies'] = movie_suggestion
							context['actors'] = [input_text,]
							user_obj.userStep = 3
							user_obj.context  = json.dumps(context)
							user_obj.save()							


							# return movies block						
							for movie in movie_suggestion:
								print movie
								message["message"]["quick_replies"].append({"content_type":"text","title":movie,"payload":movie})

							# message["message"]["quick_replies"].append({"content_type":"text","title":"something else","payload":"something else"})
							self.send_message(message,fb_id)

						elif 'genres' in context and input_text in context['genres']:
							message = {"recipient":{"id":fb_id},"message":{"text":"Almost there and Keep trying I promise you will hit your next dream movie!","quick_replies":[]}}
							#check if actor suggestion
							user_obj, Create = UserSteps.objects.get_or_create(userId=fb_id)
							movie_suggestion = []
							movie_suggestion = logic.movie_suggestion_by_genre(input_text)

							context['movies'] = movie_suggestion
							context['genres'] = [input_text,]
							user_obj.userStep = 3
							user_obj.context  = json.dumps(context)
							user_obj.save()							


							# return movies block						
							for movie in movie_suggestion:
								print movie
								message["message"]["quick_replies"].append({"content_type":"text","title":movie,"payload":movie})

							# message["message"]["quick_replies"].append({"content_type":"text","title":"something else","payload":"something else"})


							self.send_message(message,fb_id)
						




					# response_msg = json.dumps({"recipient":{"id":fb_id}, "message":{"text": check_message}})
					# status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
						
					# movie_list
					# movies_details_url = "https://graph.facebook.com/v2.6/%s/movies"%fb_id
					# movies_details_params = {'access_token':'%s' % self.access_token}
					# movies_details = requests.get(movies_details_url, movies_details_params).json()



						
		return HttpResponse()

		# movies_list_url = "https://graph.facebook.com/v2.6/%s/movies" % fb_id
		# 				movies_details_params = {'access_token':'%s' % self.access_token}
		# 				movies_details = requests.get(movies_list_url, movies_details_params).json()
		# 				post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % self.access_token
		# 				response_msg = json.dumps({"recipient":{"id":fb_id}, "message":{"text": movies_details}})


class Test(generic.View):
	def get(self, request, *args, **kwargs):
		from logic import get_movie_plot
		# print get_movie_plot("movie which involves stealing a car")
		# print get_movie_plot("movie with an alien invasion")
		return HttpResponse('test')