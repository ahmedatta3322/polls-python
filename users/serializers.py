from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    access_token = serializers.SerializerMethodField()
    refresh_token = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','is_staff', 'access_token', 'refresh_token')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def get_access_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    
    def get_refresh_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token)
    
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }