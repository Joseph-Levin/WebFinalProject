from django.contrib import admin

from .models import HouseholdModel, ListModel, ListItemModel


admin.site.register(HouseholdModel)
admin.site.register(ListModel)
admin.site.register(ListItemModel)
