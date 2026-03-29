from django.contrib import admin
from .models import User, Portfolio, Card, Response, Exercise
# Register your models here.
admin.site.register(User)
admin.site.register(Portfolio)
admin.site.register(Card)
admin.site.register(Response)
admin.site.register(Exercise)
