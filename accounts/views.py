from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from accounts.serializer import *

class UserRegistationView(APIView): 
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True,):
          
            serializer.save()
            return Response({"msg":'succesfull user saved'})
        return Response({ "msg":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth import authenticate

class UserLoginView(APIView): 
    def post(self,request,format=None):
        serializers=UserLoginSerializer(data=request.data)
        
        if serializers.is_valid(raise_exception=True):
           email=serializers.data.get('email')
           password=serializers.data.get('password')
           user=authenticate(email=email,password=password)
           
           if user is not None:
                return Response({ "msg":str(user)},status=status.HTTP_200_OK)
        return Response({ "errors":'Email or password invalid'},status=status.HTTP_200_OK)