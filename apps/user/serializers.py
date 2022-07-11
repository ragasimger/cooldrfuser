from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.authentication.staticstuffs import domain_name

class CreateSerialize(serializers.ModelSerializer):
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class UpdateSerialize(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class UserRegisterSerializer(CreateSerialize):
    password = serializers.CharField(
        style = {'input_type': 'password'},
        write_only=True,
        min_length=8
    )
    email = serializers.EmailField(
        style = {'important': True, 'input_type': 'email'},
    )
    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'username',
            'email',
            'password',
        ]

class UserUpdateSerializer(UpdateSerialize):
    profile_image = serializers.SerializerMethodField()
    image = serializers.ImageField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            "phone",
            "image",
            "profile_image",
        ]

    def get_profile_image(self, object):
        return f"{domain_name}{object.image.url}"


class AdminLevelUserSerializer(UserRegisterSerializer):
    
    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            "phone",
            "image",
            "is_active",
            "is_staff",
        ]


class ResendOtp(serializers.ModelSerializer):
    email = serializers.EmailField()
    otp = serializers.CharField(write_only=True)
    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'otp',
        ]

class VerifyOtpSerializer(ResendOtp):
    pass