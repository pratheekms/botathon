# urls for the app
from .views import MovieTimeBot, Test
from django.conf.urls import url, include

urlpatterns = [
                  url(r'^103d88ee14c3773b44fbf98bae4b646fa2095c95e2d630cc3d/?$', MovieTimeBot.as_view()), 
                  url(r'^test/?$', Test.as_view()) ,
               	
               ]