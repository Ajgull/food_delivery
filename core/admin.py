from django.contrib import admin

from core.models import Comment, Dish, Order, Profile, Restaurant

admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Dish)
admin.site.register(Order)
admin.site.register(Restaurant)
