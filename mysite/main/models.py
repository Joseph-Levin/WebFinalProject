from django.db import models
from django.contrib.auth.models import User


class HouseholdModel(models.Model):
  name = models.CharField(max_length=255)
  members = models.ManyToManyField(User)
  lists = models.ManyToManyField()

class ListModel(models.Model):
  name = models.CharField(max_length=255)
  household = models.ForeignKey(HouseholdModel, related_name='household_list')