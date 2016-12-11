from django.contrib import admin
from .models import MovieProperties, Genre, PlotLine, UserSteps
# Register your models here.

admin.site.register(MovieProperties)
admin.site.register(Genre)
admin.site.register(PlotLine)
admin.site.register(UserSteps)

