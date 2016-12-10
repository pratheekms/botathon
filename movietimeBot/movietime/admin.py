from django.contrib import admin
from .models import MovieProperties, Genre, PlotLine
# Register your models here.

admin.site.register(MovieProperties)
admin.site.register(Genre)
admin.site.register(PlotLine)

