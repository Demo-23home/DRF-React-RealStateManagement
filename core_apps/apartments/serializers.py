from rest_framework import serializers
from .models import Apartments



class ApartmentsSerializer(serializers.ModelSerializer): 
    tenant = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta: 
        model = Apartments
        exclude = ["pkid", "updated_at"]