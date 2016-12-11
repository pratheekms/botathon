from django.conf import settings
from django.shortcuts import render
from django.views import generic
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

# Create your views here.


class MovieTimeBot(generic.View):

	access_token = settings.ACCESS_TOKEN

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)


	def get(self, request, *args, **kwargs):
		"""get request to handle input from the facebook bot"""
		if self.request.GET['hub.verify_token'] == '42873292':
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error, invalid token')


	def post(self, request, *args, **kwargs):

		incoming_message = json.loads(self.request.body.decode('utf-8'))
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				if 'message' in message:
					print message, "message"
					print message['sender']['id']
					
					# step 1 replying with a user
					fb_id = message['sender']['id']
					print user_details, "user details"
					if 'first_name' in user_details:
						first_name = user_details['first_name']
						check_message = "Yo, %s!! let me get fixed you with a movie right away" % first_name
						post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % self.access_token 
						response_msg = json.dumps({"recipient":{"id":fb_id}, "message":{"text": check_message}})
						status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
		
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