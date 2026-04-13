from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk","name","surname","username","email","phone","image" ,"role"]


class UserCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name","username","password","surname","email","phone","image" ,"role"]
    
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
    new_password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        if attrs['password'] == attrs['new_password']:
            return serializers.ValidationError('parol va yangi parol teng bo\'lmasligi kerak!')
        
        return attrs

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)