from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as auth_user


from . import models


def must_be_unique(value):
  user_objects = auth_user.objects.filter(email=value)
  if len(user_objects) > 0:
    raise forms.ValidationError('Email already in use')
  return value


def unique_household_name(value):
    household_objs = models.HouseholdModel.objects.filter(name=value)
    if len(household_objs) > 0:
        raise forms.ValidationError('Household name already in use')
    return value

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        required=True,
        validators=[must_be_unique]
    )
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    class Meta:
        model = auth_user
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class HouseholdForm(forms.Form):
    name = forms.CharField(
        max_length=32,
        label='Household Name',
        required=True,
        validators=[unique_household_name]
    )


    def save(self, request):
        household_instance = models.HouseholdModel()
        household_instance.name = self.cleaned_data['name']
        household_instance.save()
        return household_instance