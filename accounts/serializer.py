from rest_framework import serializers
from accounts.models import MyUser


class UserSerializer(serializers.Serializer):
    password2 =serializers.CharField(style={
        'input_type':'password',
        'write_only':True
                  })
    
    class Meta:
        model = MyUser
        fields = ('email','name','password','password2','tc')
        extra_kwargs={
            'password':{'write_only':True}
        }