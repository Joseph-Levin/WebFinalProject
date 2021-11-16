from django.contrib import admin

from .models import HouseholdModel, HouseholdInviteModel, ListModel, ListItemModel


admin.site.register(HouseholdModel)
admin.site.register(HouseholdInviteModel)
admin.site.register(ListModel)
admin.site.register(ListItemModel)
