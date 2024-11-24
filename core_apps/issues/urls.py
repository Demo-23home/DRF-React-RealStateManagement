from django.urls import path
from .views import (
    IssueCreateAPIView,
    IssueDeleteAPIView,
    IssueDetailAPIView,
    IssuesListAPIView,
    IssueUpdateAPIView,
    AssignedIssuesListAPIView,
    MyIssuesAPIView,
)


urlpatterns = [
    path("", IssuesListAPIView.as_view(), name="issues-list"),
    path("me/", MyIssuesAPIView.as_view(), name="my-issues-list"),
    path("assigned/", AssignedIssuesListAPIView.as_view(), name="assigned-issues"),
    path("create/<uuid:apartment_id>/", IssueCreateAPIView.as_view(), name="create-issue"),
    path("update/<uuid:id>/", IssueUpdateAPIView.as_view(), name="update-issue"),
    path("<uuid:id>/", IssueDetailAPIView.as_view(), name="issue-detail"),
    path("delete/<uuid:id>/", IssueDeleteAPIView.as_view(), name="delete-issue"),
]
