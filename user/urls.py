from django.urls import path

from . import views
urlpatterns = [
    path('login', views.login_view, name='user_login'),
    path('dashboard', views.dashboard_view, name='user_dashboard'),
    path('signup', views.signup_view,name='user_signup'),
]