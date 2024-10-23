from django.contrib import admin
from django.urls import path
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="RealState API",
        default_version=1,
        description="An API App for Managing Apartments",
        contact=openapi.Contact(email="zeyadslama23@gmail.com"),
        license=openapi.License(name="MIT License")
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)


urlpatterns = [
    path("redoc/", schema_view.with_ui("redoc",
         cache_timeout=0), name="schema-redoc"),
    path(settings.ADMIN_URL, admin.site.urls),
]


admin.site.site_header = "Alpha Apartments Admin"  # Sets the header in the admin
# Sets the title on the browser tab
admin.site.site_title = "Alpha Apartments Admin Portal"
# Sets the index page title
admin.site.index_title = "Welcome to the Alpha Apartments Admin Portal"
