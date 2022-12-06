from rest_framework import serializers
from accounts.models import MyUser


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
        print(password,password2,'>>>>>>>>>>>>>>>>>>>>>>',attrs)
        if (password!=password2):
            raise serializers.ValidationError('Password dont match')
        return attrs
    
    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)