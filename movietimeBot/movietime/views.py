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
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				if 'message' in message:
					print message, "message"
					print message['sender']['id']
					# step 1 replying with a user
					fb_id = message['sender']['id']
					usersteps_obj, Create = UserSteps.objects.get_or_create(userId=fb_id)
					if message['message']['text'] == "Hey":
						print "check"
						message = {"recipient":{"id":fb_id},"message":{"text":"Hey there . I am Movie PIRATE. I am here to help you find a good movie. You can just tell me what you want, in a good movie and il be picking for you. It could be something like 'A movie which involves stealing a car' or you can select one of these to search as well","quick_replies":[{"content_type":"text","title":"Actor","payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"},{"content_type":"text","title":"Genre","payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"},]}}
						self.send_message(message,fb_id)
						user_obj, Create = UserSteps.objects.get_or_create(userId=fb_id)
						user_obj.userStep = 1
						user_obj.context = json.dumps({})
						user_obj.save()

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

						message["message"]["quick_replies"].append({"content_type":"text","title":"something else","payload":"something else"})
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
						message = {"recipient":{"id":fb_id},"message":{"text":'Genre'}}
						self.send_message(message,fb_id)
						user_obj, Create = UserSteps.objects.get_or_create(userId=fb_id)
						user_obj.userStep = 2



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
							
							hotstar = hotstar_scrape(input_payload)
							hotstar_status = hotstar.scrape()
							netflix = netflix_scrape(input_payload)
							netflix_status = netflix.scrape()
							pvr = pvr_scrape(input_payload)
							pvr_status = pvr.scrape()
							more_movies = taste_kid.get_tastekid_movie([input_payload,])

							# p_id1 = Process(target = hotstar.scrape, args=())
							# p_id2 = Process(target = netflix.scrape, args=())
							# p_id3 = Process(target = pvr.scrape, args=())

							# p_id1.start()
							# p_id2.start()
							# p_id3.start()
							print more_movies
							print hotstar_status
							print netflix_status
							print pvr_status

							message = {
										 "recipient":{
										   "id":fb_id
										 },
										 "message":{
										   "attachment":{
										     "type":"image",
										     "text":netflix_status,
										     "payload":{
										       "url":"https://lh5.googleusercontent.com/-9El0rLwfX5E/AAAAAAAAAAI/AAAAAAAAIl8/S4IbyT2gTMo/s0-c-k-no-ns/photo.jpg"
										     }
										   }
										 }
										}
							self.send_message(message,fb_id)
						elif 'actors' in context and input_text in context['actors']:

							message = {"recipient":{"id":fb_id},"message":{"text":"Do you like any of these movies?","quick_replies":[]}}
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

							message["message"]["quick_replies"].append({"content_type":"text","title":"something else","payload":"something else"})


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