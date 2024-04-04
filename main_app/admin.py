from django.contrib import admin
from .models import Game, Developer, Type

# Register your models here.
admin.site.register(Game)
admin.site.register(Developer)
admin.site.register(Type)
