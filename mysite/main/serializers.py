# Guidance from https://www.django-rest-framework.org/tutorial/1-serialization/ 
from django.contrib.auth.models import User
from .models import ListItemModel
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ListItemSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = ListItemModel
        fields = ['pk', 'description', 'price', 'complete', 'list', 'author', 'receipt']