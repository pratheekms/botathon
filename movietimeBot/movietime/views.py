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
					print message['sender']['id']
					fb_id = message['sender']['id']
					user_details_url = "https://graph.facebook.com/v2.6/%s"%fb_id
					user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':'%s' % self.access_token}
					user_details = requests.get(user_details_url, user_details_params).json()
					print user_details
					first_name = user_details['first_name']
					check_message = "Yo, %s!!" % first_name
					post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % self.access_token 
					response_msg = json.dumps({"recipient":{"id":fb_id}, "message":{"text": check_message}})
					status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
					return HttpResponse()


