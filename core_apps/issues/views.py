import logging
from typing import Any
from django.http import Http404
from django.utils import timezone
from rest_framework import status, generics, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from core_apps.apartments.models import Apartments
from core_apps.common.models import ContentView
from core_apps.common.renderers import GenericJSONRenderer
from .emails import send_issue_confirmation_email, send_issue_resolved_email
from .models import Issue
from .serializers import IssueSerializer, IssueUpdateSerializer
from django.contrib.contenttypes.models import ContentType

logger = logging.getLogger(__name__)


class IsSuperUserOrStaff(permissions.BasePermission):
    def __init__(self) -> None:
        self.message = None

    def has_permission(self, request, view):
        is_authorized = (
            request.user
            and request.user.is_authenticated
            and (request.user.is_superuser or request.user.is_staff)
        )
        if not is_authorized:
            message = "Accessing this information is restricted to staff and admin users only! "
        return is_authorized


class IssuesListAPIView(generics.ListAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    renderer_classes = [GenericJSONRenderer]
    permission_classes = [IsSuperUserOrStaff]
    object_label = "issues"


class AssignedIssuesListAPIView(generics.ListAPIView):
    serializer_class = IssueSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "assigned_issues"

    def get_queryset(self):
        user = self.request.user
        issues = Issue.objects.filter(assigned_to=user)
        return issues


class MyIssuesAPIView(generics.ListAPIView):
    serializer_class = IssueSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "my_issues"

    def get_queryset(self):
        user = self.request.user
        issues = Issue.objects.filter(reported_by=user)
        return issues


class IssueCreateAPIView(generics.CreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "issue"

    def perform_create(self, serializer: IssueSerializer) -> None:
        apartment_id = self.kwargs.get("apartment_id")

        if not apartment_id:
            raise ValidationError({"apartment_id": ["Apartment ID is required."]})
        try:
            apartment = Apartments.objects.get(
                id=apartment_id, tenant=self.request.user
            )
        except Apartments.DoesNotExist:
            raise PermissionDenied(
                "You do not have permission to report an issue for this apartment. its not yours"
            )

        issue = serializer.save(reported_by=self.request.user, apartment=apartment)

        send_issue_confirmation_email(issue)


class IssueDetailAPIView(generics.RetrieveAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    lookup_field = "id"
    renderer_classes = [GenericJSONRenderer]
    object_label = "issue"

    def get_object(self) -> Issue:
        issue = super().get_object()
        user = self.request.user

        if not (
            issue.reported_by == user or issue.assigned_to == user or user.is_staff
        ):
            raise PermissionDenied("You don't have permission to view this issue!. ")
        self.record_issue_view(issue)
        return issue

    def record_issue_view(self, issue: Issue):
        content_type = ContentType.objects.get_for_model(issue)
        viewer_ip = self.get_client_ip()

        obj, created = ContentView.objects.update_or_create(
            content_type=content_type,
            user=self.request.user,
            object_id=issue.pk,
            viewer_ip=viewer_ip,
            defaults={"last_viewed": timezone.now()},
        )

    def get_client_ip(self) -> str:
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR")
        return ip


class IssueUpdateAPIView(generics.UpdateAPIView):
    queryset = Issue.objects.all()
    lookup_field = "id"
    serializer_class = IssueUpdateSerializer
    renderer_classes = [GenericJSONRenderer]

    def get_object(self):
        issue = super().get_object()
        user = self.request.user

        if not (issue.assigned_to == user):
            logger.warning(
                f"Unauthorized issue update attempt  by user {user.get_full_name} on issue {issue.title}"
            )
            raise PermissionDenied("You don't have permission to update this issue")
        send_issue_resolved_email(issue)
        return issue


class IssueDeleteAPIView(generics.DestroyAPIView):
    queryset = Issue.objects.all()
    lookup_field = "id"
    serializer_class = IssueSerializer

    def get_object(self) -> Issue:
        try:
            issue = super().get_object()
        except Http404:
            raise Http404("Issue not found") from None
        user = self.request.user
        if not (user == issue.reported_by or user.is_staff):
            logger.warning(
                f"Unauthorized delete attempt by user {user.get_full_name} on issue {issue.title}"
            )
            raise PermissionDenied("You do not have permission to delete this issue")
        return issue

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        super().delete(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
