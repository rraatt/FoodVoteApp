from django.contrib import admin

from foodapp.models import Restaurant, Menu, Vote

admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Vote)
# Register your models here.
