from django.db import models
import logging
from typing import Any
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core_apps.apartments.models import Apartments
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from config.settings.local import SITE_NAME, DEFAULT_FROM_EMAIL
from core_apps.common.models import TimeStampedModel

User = get_user_model()
logger = logging.getLogger(__name__)


class Issue(TimeStampedModel):

    class IssueStatus(models.TextChoices):
        REPORTED = ("reported", _("Reported"))
        RESOLVED = ("resolved", _("Resolved"))
        IN_PROGRESS = ("in_progress", _("In Progress"))

    class Priority(models.TextChoices):
        LOW = ("low", _("Low"))
        MEDIUM = ("medium", _("Medium"))
        HIGH = ("high", _("High"))

    apartment = models.ForeignKey(
        Apartments, verbose_name=_("Apartment"), on_delete=models.CASCADE, related_name="issues"
    )
    reported_by = models.ForeignKey(
        User,
        verbose_name=_("Reported By"),
        on_delete=models.CASCADE,
        related_name="reported_by_issues",
    )
    assigned_to = models.ForeignKey(
        User,
        verbose_name=_("Assigned To"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_to_issues",
    )

    title = models.CharField(_("Title"), max_length=250)
    description = models.TextField(_("Issue Description"))
    status = models.CharField(
        _("Status"), max_length=50, choices=IssueStatus.choices, default=IssueStatus.REPORTED
    )
    priority= models.CharField(_("Priority"), max_length=50, choices=Priority.choices, default=Priority.LOW)
    resolved_on = models.DateField(_("Resolved On "),null=True, blank=True)

    def __str__(self) -> str: 
        return self.title

    def save(self, *args, **kwargs) -> None: 
        is_existing_instance = self.pk is not None
        old_assigned_to = None

        if is_existing_instance: 
            old_issue = Issue.objects.get(pk=self.pk)
            old_assigned_to = old_issue.assigned_to
            super().save(*args, **kwargs)

        if (is_existing_instance and self.assigned_to is not None and self.assigned_to != old_assigned_to):
            self.notify_assigned_user()

    def notify_assigned_user(self) -> None: 
        try: 
            subject = "A new issue assigned {self.title}"
            from_email = DEFAULT_FROM_EMAIL
            recipient_list = [self.assigned_to.email]
            context = {"issue": self, "site_name": SITE_NAME}

            html_email = render_to_string("emails/issue_assignment_notification.html", context)

            text_email = strip_tags(html_email)
            email = EmailMultiAlternatives(subject, text_email, from_email, recipient_list)
            email.attach_alternative(html_email, "text/html")
            email.send()
        except Exception as e: 
            logger.error(f"Failed to send issue assignment email for issue: '{self.title}' due problem: {e}")
