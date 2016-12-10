from django.shortcuts import render
from django.views import generic
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

class MovieTimeBot(generic.View):

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
					print message
					user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
			return HttpResponse()


