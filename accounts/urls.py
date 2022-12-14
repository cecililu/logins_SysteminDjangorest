from django.urls import path,include
from . views import *

urlpatterns = [
    path('register',UserRegistationView.as_view()),
    path('login',UserLoginView.as_view()),
    path('user',UserProfileView.as_view()),
    path('changepassword',UserChangePasswordview.as_view()),
    path('sendresetemail',SendPasswordResetView.as_view()),
    path('reset/<uid>/<token>',ChangePasswordViewEmail.as_view())
]
