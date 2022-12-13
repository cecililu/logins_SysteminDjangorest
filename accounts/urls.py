from django.urls import path,include

from . views import *


urlpatterns = [
    path('register',UserRegistationView.as_view()),
      path('login',UserLoginView.as_view()),
       path('user',UserProfileView.as_view())
]
