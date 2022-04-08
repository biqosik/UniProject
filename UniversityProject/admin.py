from django.contrib import admin

from .models import Room, Topic, Message, User, Blockchain, CurrencyStock

admin.site.register(Room)
admin.site.register(Blockchain)
admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(CurrencyStock)