from rest_framework import serializers
from accounts.models import MyUser

from  django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError

from  django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
#Sereializers 
#registartion of user
class UserRegistrationSerializer(serializers.ModelSerializer):     
    password2 =serializers.CharField(style={
        'input_type':'password',
        'write_only':True 
                  })
    
    class Meta:
        model = MyUser
        fields = ('email','name','password','password2','tc')
        extra_kwargs={
            'password2':{'write_only':True}
        }   
        
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if (password!=password2):
            raise serializers.ValidationError('Password dont match')
        return attrs
    
    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)
    

#User login serializer
class UserLoginSerializer(serializers.ModelSerializer):  
    
    email=serializers.EmailField(
        max_length=255
    )
    class Meta:
        model = MyUser
        fields = ('email','password',)
           
class UserProfileSerializer(serializers.ModelSerializer):  
    class  Meta:
        model=MyUser
        fields=['id','email','name']

class ChangeUserSerializer(serializers.Serializer):  
    password=serializers.CharField(max_length=100,style={
        'input_type':'password',
        'write_only':True 
                  })
    
    password2=serializers.CharField(style={
        'input_type':'password',
        'write_only':True 
                  })
    
    class Meta:
        fields=['password','password2']
    
    
    def validate(self, attrs): 
        user=self.context.get('user')
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password!=password2:
            raise serializers.ValidationError("wait pasword dont matchin first place")
        
        user.set_password(password)
        user.save()
        return (attrs)  
import os
from accounts.utils import Util

class SendPasswordResetViewSerializer(serializers.Serializer):
    
    email=serializers.EmailField(max_length=255)   
    class Meta:
        fields=['email']
        
    def validate(self, attrs):
        email=attrs.get('email')
        if MyUser.objects.filter(email=email).exists():
            user=MyUser.objects.get(email=email)
            
            uid=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            link='http://localhost:3000/api/user/reset/'+uid+'/'+token
            
            data={'subject':'Password Reset Link',"body":link,"to_email":email}
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError("That email is not a registered user")
        return attrs
        
class ChangePasswordViewEmailSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=100,style={
        'input_type':'password',
        'write_only':True 
                  })
    
    password2=serializers.CharField(style={
        'input_type':'password',
        'write_only':True 
                  })
    
    class Meta:
        fields=['password','password2']
    
    def validate(self, attrs): 
        try:
            uid=self.context.get('uid')
            token=self.context.get('token')
            
            password=attrs.get('password')
            password2=attrs.get('password2')
            
            if password!=password2:
                raise serializers.ValidationError("wait pasword dont matchin first place")
            
            id=smart_str(urlsafe_base64_decode(uid))
            user=MyUser.objects.get(id=id)
            
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError("Not the right token")
            user.set_password(password)
            user.save()
            return (attrs)  
        
        except DjangoUnicodeDecodeError as idenifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError("Invalid token")
            
            