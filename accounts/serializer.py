from rest_framework import serializers
from accounts.models import MyUser
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
        user.save
        return (attrs)  
        
       