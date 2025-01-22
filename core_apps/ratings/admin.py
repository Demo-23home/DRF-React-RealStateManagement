from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from .models import Rating
from django.db.models import Avg, QuerySet


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = [
        "rated_user",
        "rated_user",
        "rating",
        "comment",
        "get_average_rating",
    ]
    search_fields = ["rated_user__username", "rating_user__username"]
    list_filter = ["rating", "created_at"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            average_rating=Avg("rated_user__received_ratings__rating")
        )
        return queryset

    def get_average_ratings(self, obj):
        return round(obj.average_rating, 2) if obj.average_rating is not None else None

    get_average_ratings.short_description = "Average Ratings"
    get_average_ratings.admin_order_field = "average_rating"
