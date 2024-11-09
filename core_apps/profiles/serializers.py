from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from .models import Profile
from core_apps.apartments.serializers import ApartmentsSerializer

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    username = serializers.ReadOnlyField(source="user.username")
    full_name = serializers.ReadOnlyField(source="user.full_name")
    country = CountryField(name_only=True)
    date_joined = serializers.DateTimeField(source="user.date_joined", read_only=True)
    avatar = serializers.SerializerMethodField()
    apartment = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "id",
            "slug",
            "first_name",
            "last_name",
            "username",
            "full_name",
            "country",
            "city_of_origin",
            "bio",
            "gender",
            "occupation",
            "reputation",
            "date_joined",
            "avatar",
            "apartment"
        ]

    def get_avatar(self, obj: Profile) -> None:
        try:
            return obj.avatar.url
        except AttributeError:
            return None

    def get_apartment(self, obj): 
        apartment = obj.user.apartment.first()
        if apartment: 
            return ApartmentsSerializer(apartment).data
        return None

class UpdateProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    username = serializers.CharField(source="user.username")
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "username",
            "country",
            "city_of_origin",
            "bio",
            "gender",
            "occupation",
            "phone_number",
        ]


class AvatarUploadSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Profile
        fields = ["avatar"]
