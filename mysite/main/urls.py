from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',  auth_views.LoginView.as_view()),
    path('register/', views.register),
    path('logout/', views.logout_view),
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url='/')),
    path('household/', views.household),
    path('household/<int:id>/', views.household_home),
    path('household/<int:id>/invite/', views.household_invite),
    path('household/<int:id>/list/', views.new_list),
    path('household/<int:id>/list/<int:listid>/', views.view_list),
    path('household/<int:id>/list/<int:listid>/delete/', views.delete_list),
    path('household/<int:id>/list/<int:listid>/listitem/<int:itemid>/toggle/', views.list_item_toggle),
    path('household/<int:id>/list/<int:listid>/listitem/<int:itemid>/delete/', views.list_item_delete),
    path('household/<int:id>/list/<int:listid>/listitem/<int:itemid>/edit/', views.list_item_edit),
    path('profile/', views.profile),
    path('update_profile/', views.update_profile),
    path('accept/<int:id>', views.accept_invite),
    path('decline/<int:id>', views.decline_invite),
    path('leave_household/<int:id>', views.leave_household),
    path('json/list/<int:listid>/', views.list_json),

]