from django.db import models
from core_apps.common.models import TimeStampedModel
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Report(TimeStampedModel):
    title = models.CharField(verbose_name=_("Title"), max_length=225)
    slug = AutoSlugField(populate_from="title", unique=True)
    reported_by = models.ForeignKey(User, verbose_name=_("Reported By"), on_delete=models.CASCADE, related_name="reports_made")
    reported_user = models.ForeignKey(User, verbose_name=_("Reported User"), on_delete=models.CASCADE, related_name="reports_received")
    description = models.TextField(_("Description"))
    
    def __str__(self) -> str:
        return f"Report by {self.reported_by.get_full_name} against {self.reported_user.get_full_name}"


    class Meta: 
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        ordering = ["-created_at"]