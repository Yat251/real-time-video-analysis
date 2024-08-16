from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class UserEventSerializer(serializers.HyperlinkedModelSerializer):  # serializers.ModelSerializer
    class Meta:
        model = UserEvent
        fields = ['id', 'user', 'video', 'duration', 'created_at']

class VideoSerializer(serializers.HyperlinkedModelSerializer):  # serializers.ModelSerializer
    class Meta:
        model = Video
        fields = ['id', 'videofile', 'watches', 'created_at']

class UserSessionSerializer(serializers.HyperlinkedModelSerializer):  # serializers.ModelSerializer
    class Meta:
        model = UserSession
        fields = ['id', 'user', 'session', 'duration', 'created_at']


