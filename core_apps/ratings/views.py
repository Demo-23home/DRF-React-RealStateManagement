from .models import Rating
from .serializers import RatingSerializer
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from rest_framework.response import Response
from core_apps.common.renderers import GenericJsonRenderer
from core_apps.profiles.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class RatingCreateAPIView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    object_label = "rating"
    renderer_classes = [GenericJsonRenderer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rated_user_username = request.data.get("rated_user_username")

        try:
            rated_user = User.object.get(username=rated_user_username)
        except User.DoesNotExist:
            raise NotFound(f" A user with this username doesn't exist!.")

        rating_user = request.user

        if rating_user == rated_user:
            raise PermissionDenied("You can't rate your self!.")

        try:
            rated_user_occupation = rated_user.profile.occupation
            rating_user_occupation = rating_user.profile.occupation
        except Profile.DoesNotExist:
            raise ValidationError("A user must have a valid profile!.")

        if (rated_user_occupation == Profile.Occupation.TENANT) and (
            rating_user_occupation == Profile.Occupation.TENANT
        ):
            raise PermissionDenied("A tenant can't review another tenant")

        allowed_occupations = [
            Profile.Occupation.Carpenter,
            Profile.Occupation.Electrician,
            Profile.Occupation.HAVC,
            Profile.Occupation.Mason,
            Profile.Occupation.Painter,
            Profile.Occupation.Plummer,
            Profile.Occupation.Roofer,
        ]

        if (rating_user_occupation == Profile.Occupation.TENANT) and (
            rated_user_occupation not in allowed_occupations
        ):
            raise ValidationError(
                "A tenant can only review technicians and not other tenants"
            )

        if (rating_user_occupation != Profile.Occupation.TENANT) and (
            rating_user == rated_user
        ):
            raise PermissionDenied("A technician can't review themselves!.")

        if (rating_user_occupation != Profile.Occupation.TENANT) and (
            rated_user_occupation != Profile.Occupation.TENANT
        ):
            raise PermissionDenied("A technician can't review another technician!.")
        
        rating = serializer.save(rating_user=rating_user, rated_user=rated_user)
        serializer = self.get_serializer(rating)
        headers = self.get_success_headers(serializer.data)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)