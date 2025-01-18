from .serializers import ReportSerializer
from .models import Report
from rest_framework import serializers, generics
from core_apps.common.renderers import GenericJsonRenderer


class ReportCreateAPIView(generics.CreateAPIView):
    queryset = Report.objects.all()
    renderer_classes = [GenericJsonRenderer]
    serializer_class = ReportSerializer
    object_label = "report"

    def perform_create(self, serializer: serializers.Serializer) -> None:
        serializer.save(reported_by=self.request.user)


class ReportListAPIView(generics.ListAPIView):
    renderer_classes = [GenericJsonRenderer]
    serializer_class = ReportSerializer
    object_label = "reports"

    def get_queryset(self) -> Report:
        user = self.request.user
        my_reports = Report.objects.filter(reported_by=user)
        return my_reports
