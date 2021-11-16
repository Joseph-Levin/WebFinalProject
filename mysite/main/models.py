from django.db import models
from django.contrib.auth.models import User


class HouseholdModel(models.Model):
  name = models.CharField(max_length=255)
  members = models.ManyToManyField(User, related_name='members')

  def __str__(self):
    return self.name


# class HouseholdMemberModel(models.Model):
#   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
#   household = models.ForeignKey(HouseholdModel, on_delete=models.CASCADE, related_name='member')

class ListModel(models.Model):
  name = models.CharField(max_length=255, unique=True)
  household = models.ForeignKey(HouseholdModel, on_delete=models.CASCADE, related_name='list')

  def __str__(self):
    return self.name

class ListItemModel(models.Model):
  description = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
  complete = models.BooleanField(default=False)
  list = models.ForeignKey(ListModel, on_delete=models.CASCADE, related_name='item')
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='item')

  def __str__(self):
    return self.description
  

class HouseholdInviteModel(models.Model):
  household = models.ForeignKey(HouseholdModel, on_delete=models.CASCADE)
  invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitee')
  inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inviter')
  message = models.CharField(max_length=1024)

  def __str__(self):
    return "From " + str(self.inviter) + " to " + str(self.invitee) + " for " + str(self.household)