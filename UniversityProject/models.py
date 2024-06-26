from django.db import models
from django.contrib.auth.models import AbstractUser
from embed_video.fields import EmbedVideoField

class User(AbstractUser):
    name = models.CharField(max_length=256, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Room(models.Model):
    host =models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic =models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]

    class Meta:
        ordering = ['-updated', '-created']

class Blockchain(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cryptocurrency = models.CharField(max_length=256, null=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, default="avatar.svg")
    short = models.CharField(max_length=15, null=True)
    timeframe = models.DateTimeField(null=True)

    def __str__(self):
        return self.short

    class Meta:
        ordering = ['pk']


class News(models.Model):
    topic = models.CharField(max_length=256, null=True)
    info = models.TextField(null=True, blank=True)
    video = EmbedVideoField(null=True, blank=True)

    def __str__(self):
        return self.topic

class CurrencyStock(models.Model):
    currency = models.CharField(max_length=255, null=True)
    yes = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.yes