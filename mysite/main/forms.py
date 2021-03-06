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


class HouseholdForm(forms.ModelForm):
    class Meta:
        model = models.HouseholdModel
        fields = ('name', 'icon')

    def save(self, commit=True):
        household = super(HouseholdForm, self).save()
        return household


class HouseholdInviteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.userid = kwargs.pop('userid', None)
        self.houseid = kwargs.pop('houseid', None)
        super(HouseholdInviteForm, self).__init__(*args, **kwargs)
        self.fields['invitee'].queryset = models.User.objects.exclude(invitee__in=models.HouseholdInviteModel.objects.filter(household=self.houseid)).exclude(members__id=self.houseid)
        print(self.fields['invitee'].queryset)

    class Meta:
        model=models.HouseholdInviteModel
        fields = ['invitee', 'message']


    invitee = forms.ModelChoiceField(queryset=None)
    message = forms.CharField(max_length=1024)

    def save(self, request):
            invite_instance = models.HouseholdInviteModel()
            invite_instance.invitee = self.cleaned_data['invitee']
            invite_instance.message = self.cleaned_data['message']
            invite_instance.inviter = request.user
            invite_instance.household = models.HouseholdModel.objects.get(pk=self.houseid)
            invite_instance.save()
            return invite_instance


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = auth_user
        fields = ['username', 'email', 'first_name', 'last_name']


class ListForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.houseid = kwargs.pop('houseid', None)
        kwargs.update(initial={
                'household': self.houseid,
            })

        super(ListForm, self).__init__(*args, **kwargs)


    class Meta:
        model = models.ListModel
        fields = '__all__'
        widgets = {
            'household': forms.HiddenInput(),
            }


class ListItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance is None:
            self.userid = kwargs.pop('userid', None)
            self.listid = kwargs.pop('listid', None)
            kwargs.update(initial={
                    'list': self.listid,
                    'author': self.userid,
                })

        super(ListItemForm, self).__init__(*args, **kwargs)


    class Meta:
        model = models.ListItemModel
        fields = '__all__'
        widgets = {
            'complete': forms.HiddenInput(),
            'list': forms.HiddenInput(),
            'author': forms.HiddenInput(),
            }
