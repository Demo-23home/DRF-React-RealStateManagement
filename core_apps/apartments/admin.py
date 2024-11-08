from django.contrib import admin
from .models import Apartments

# Register your models here.


@admin.register(Apartments)
class Apartments(admin.ModelAdmin):
    list_display = ["id", "unit_number", "floor", "tenant"]
    list_display_links = ["id", "unit_number"]
    list_filter = ["building", "floor"]
    search_fields = ["unit_number"]
    ordering = ["building", "floor"]
    autocomplete_fields = ["tenant"]
