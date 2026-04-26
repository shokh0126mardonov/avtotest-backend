from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import DeviceLock

User = get_user_model()


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk","name","surname","username","email","phone","image" ,"role"]


class UserCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk","name","username","password","surname","email","phone","image" ,"role"]
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)

        user.save()

        return user

class GetByUsername(serializers.Serializer):
    username = serializers.CharField(max_length=150)

class UserSetPasswordSerializers(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    confirm = serializers.CharField(max_length=128)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm']:
            raise serializers.ValidationError("Parol va confirm parol teng bo'lishi kerak!")
        
        return attrs

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        
        if password:
            instance.set_password(password) 
            instance.save()
        
        return instance


class LoginSerializers(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)
    device_id = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    telegram_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = DeviceLock
        fields = ['username','password','device_id','user_agent','created_at','telegram_id']

    def validate(self, attrs):
        device_id = attrs.get('device_id')
        telegram_id = attrs.get('telegram_id')

        if not device_id and telegram_id is None:
            raise serializers.ValidationError(
                "telegram_id yoki device_id dan bittasi yuborilishi shart!"
            )

        return attrs
