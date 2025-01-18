from django.urls import path
from .views import ReportCreateAPIView, ReportListAPIView


urlpatterns = [
    path("me/", ReportListAPIView.as_view(), name="get-my-reports"),
    path("create/", ReportCreateAPIView.as_view(), name="create-report")
]
