from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from accounts.serializer import *
from accounts.renderer import UserRender
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    referesh=RefreshToken.for_user(user)
    return {
        'refresh':str(referesh),
        'access':str(referesh.access_token)
    }
    
class UserRegistationView(APIView): 
    renderer_classes=[UserRender]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True,):
            user=serializer.save()
            token=get_tokens_for_user(user) 
            return Response({"msg":'succesfull user saved','token':token})
        return Response({ "msg":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    
from django.contrib.auth import authenticate
class UserLoginView(APIView):
    renderer_classes=[UserRender] 
    def post(self,request,format=None):
        serializers=UserLoginSerializer(data=request.data)  
        if serializers.is_valid(raise_exception=True):
           email=serializers.data.get('email')
           password=serializers.data.get('password')
           user=authenticate(email=email,password=password)
           if user is not None:
                token=get_tokens_for_user(user) 
                return Response({"msg":'succesfull loged in','token':token})
        return Response({ "errors":'Email or password invalid'},status=status.HTTP_200_OK)
    
    
        
class UserProfileView(APIView):
     renderer_classes=[UserRender]
     permission_classes=[IsAuthenticated]
     def get(self,request,format=None):
          serializers=UserProfileSerializer(request.user)
          return Response (serializers.data,status=status.HTTP_200_OK)
  
  
class UserChangePasswordview(APIView):
    renderer_classes=[UserRender]
    permission_classes=[IsAuthenticated]
        
    def post(self,request,format=None):
        serializers=ChangeUserSerializer(data=request.data,context={'user':request.user})
        if serializers.is_valid(raise_exception=True):
            return Response({"msg":'password changed succesfull'})
        return Response(serializers.errors)

class SendPasswordResetView(APIView):
    renderer_classes=[UserRender]    
    def post(self,request,format=None):
        serializers=SendPasswordResetViewSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            return Response({"msg":'email sen to reset password'})

class ChangePasswordViewEmail(APIView):
    renderer_classes=[UserRender] 
    
    def post(self,request,uid,token,format=None): 
        serializers=ChangePasswordViewEmailSerializer(data=request.data,
                                                      context={'uid':uid,"token":token})
        
        if serializers.is_valid(raise_exception=True):
            return Response({"msg":'password change success'})
       
    