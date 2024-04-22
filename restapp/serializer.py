from rest_framework import serializers
from .models import UserRegistration, Role
from django.contrib.auth.hashers import make_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = UserRegistration
        fields = ['username', 'email', 'password', 'age', 'role_name']

    def create(self, validated_data):
        role_name = validated_data.pop('role_name')
        role, _ = Role.objects.get_or_create(name=role_name)
        validated_data['password'] = make_password(validated_data['password'])
        user = UserRegistration.objects.create(**validated_data, role=role)
        return user

        
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)
    
    
    
class UserRegistrationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegistration
        fields = ['id', 'username', 'email', 'age', 'role']

class UserRegistrationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegistration
        fields = ['email', 'age', 'role']

class UserRegistrationDeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())
