from django.contrib.auth import get_user_model
from .models import Report
from rest_framework import serializers

User = get_user_model()

class ReportSerializer(serializers.ModelSerializer): 
    reported_user_username = serializers.CharField(write_only=True)
    
    class Meta: 
        model = Report 
        fields = ["id", "title", "description", "reported_user_username", "created_at"]
        
    def validate_reported_user_username(self, value): 
        if not User.objects.filter(username=value).exists(): 
            raise serializers.ValidationError("A user with this username doesn't exist!.")
        
        return value
    
    def create(self, validated_data:dict) -> Report: 
        reported_user_username = validated_data.pop("reported_user_username")
        try: 
            reported_user = User.objects.get(username=reported_user_username)
        except User.DoesNotExist: 
            raise serializers.ValidationError("A user with this username doesn't exist!.")
        report = Report.objects.create(reported_user=reported_user, **validated_data)
        
        return report
