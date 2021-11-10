from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',  auth_views.LoginView.as_view()),
    path('register/', views.register_view),
    path('logout/', views.logout_view),
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url='/')),
    path('household/', views.household_view),

]