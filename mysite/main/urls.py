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
    path('household_invite/', views.household_invite),
    path('profile/', views.profile),
    path('update_profile/', views.update_profile),
    path('accept/<int:id>', views.accept_invite),
    path('decline/<int:id>', views.decline_invite),
    path('leave_household/<int:id>', views.leave_household),

]