from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

User = get_user_model()


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "username", "first_name", "last_name", "password"]


class CustomUserSerializer(UserSerializer):
    full_name = serializers.ReadOnlyField(source="get_full_name")
    gender = serializers.ReadOnlyField(source="profile.gender")
    slug = serializers.ReadOnlyField(source="profile.slug")
    occupation = serializers.ReadOnlyField(source="profile.occupation")
    phone_number = PhoneNumberField(source="profile.phone_number")
    country = CountryField(source="profile.country")
    city = serializers.ReadOnlyField(source="profile.city_of_origin")
    avatar = serializers.SerializerMethodField()
    reputation = serializers.ReadOnlyField(source="profile.reputation")

    class Meta(UserSerializer.Meta):
        model = User
        fields = ["id", "full_name", "email", "gender", "slug", "occupation",
                  "phone_number", "country", "city", "avatar", "reputation", "date_joined"]

        read_only_fields = ["id", "email", "date_joined"]

    def get_avatar(self, obj) -> None:
        if obj.profile.avatar: 
            return obj.profile.avatar.url
        return None