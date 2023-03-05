from rest_framework import serializers
import datetime
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'gender',
                  'date_of_birth', 'password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_date_of_birth(self, value):
        today = datetime.date.today()
        age = today.year - value.year - \
            ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError(
                'You must be at least 18 years old to register')
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            gender=validated_data['gender'],

            date_of_birth=validated_data['date_of_birth'],
            password=validated_data['password']
        )
        return user


class UserPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True)
    new_password = serializers.CharField(max_length=128, write_only=True)

    def validate_old_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Incorrect old password.')
        return value

    def validate_new_password(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("Password is too short.")
        else:
            return value


class UserProfileSerializer(serializers.ModelSerializer):
    # posts_count = serializers.IntegerField(read_only=True)
    # followers_count = serializers.IntegerField(read_only=True)
    # following_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'date_of_birth', 'gender', 'profile_pic', 'about_me',)


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    # posts_count = serializers.IntegerField(read_only=True)
    # followers_count = serializers.IntegerField(read_only=True)
    # following_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'profile_pic', 'about_me',)