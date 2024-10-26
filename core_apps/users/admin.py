from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = [
        "pkid",
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_superuser",
    ]

    search_fields = ["first_name", "last_name", "email", "username"]

    list_display_links = ["pkid", "id", "username", "email"]
    ordering = ["pkid"]

    # fieldsets is list of fields to be displayed in the user admin change form,
    # each is a tuple contains a title and a dict witch contains the fields to be displayed.
    fieldsets = (
        (_("Login Credentials"), {"fields": ("email", "password")}),
        (
            _("Personal Information"),
            {"fields": ("first_name", "last_name", "username")},
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "is_staff",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "username",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )
