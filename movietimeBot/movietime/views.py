from django.conf import settings
from django.shortcuts import render
from django.views import generic
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from pymessenger.bot import Bot

# Create your views here.


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
					# user_details_url = "https://graph.facebook.com/v2.6/%s"%fb_id
					# user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':'%s' % self.access_token}
					# user_details = requests.get(user_details_url, user_details_params).json()
					# print user_details, "user details"
					# if 'first_name' in user_details:
					# 	first_name = user_details['first_name']
					if message['text'] == "Hey":
						check_message = "Hey there . I am Movie PIRATE. I am here to help you find a good movie. You can just tell me what you want, in a good movie and il be picking for you. It could be something like 'A movie which involves stealing a car' or you can select one of these to search as well" 
						self.bot.send_text_message(fb_id, check_message)
					
					else:
						pass 
					# message = {"recipient":{"id":fb_id}, "message":{"text": check_message}}
					# self.send_message(message, fb_id)

					# check_message = {"recipient":{"id":fb_id}, "message": {"text":"or you can select one of these options to search as well","quick_replies":[{"content_type":"text","title":"Actor","payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"},{"content_type":"text","title":"Genre","payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"}, {"content_type":"text","title":"Director","payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_DIRECTOR"}]}}
					# self.send_message(check_message,fb_id)









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


