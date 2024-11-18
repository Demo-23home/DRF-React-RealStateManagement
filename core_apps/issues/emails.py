import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from config.settings.local import SITE_NAME, DEFAULT_FROM_EMAIL
from .models import Issue


logger = logging.getLogger(__name__)


def send_issue_confirmation_email(issue: Issue) -> None:
    try:
        subject = "Issue Report Confirmation"
        context = {"site_name": SITE_NAME, "issue": issue}
        html_email = render_to_string("emails/issue_confirmation.html", context)
        plain_message = strip_tags(html_email)
        from_email = DEFAULT_FROM_EMAIL
        to = [issue.assigned_to]
        email = EmailMultiAlternatives(subject, plain_message, from_email, to)
        email.attach_alternative(html_email, "text/html")
        email.send()
    except Exception as e:
        logger.error(
            f"Failed to send a confirmation email for issue: {issue.title} with error: {e}",
            exc_info=True,
        )


def issue_resolved_email(issue: Issue):
    try:
        subject = "Issue Resolved"
        context = {"site_name": SITE_NAME, "issue": issue}
        html_email = render_to_string("emails/issue_resolved_notification.html", context)
        plain_message = strip_tags(html_email)
        from_email = DEFAULT_FROM_EMAIL
        to = [issue.assigned_to]
        email = EmailMultiAlternatives(subject, plain_message, from_email, to)
        email.attach_alternative(html_email, "text/html")
        email.send()

    except Exception as e:
        logger.error(
            f"Failed to send a resolved email for issue: {issue.title} with error: {e}",
            exc_info=True,
        )


def send_resolution_email(issue: Issue):
    try:
        subject = "Issue Resolved"
        context = {"site_name": SITE_NAME, "issue": issue}
        html_email = render_to_string("emails/issue_resolved_notification.html", context)
        plain_text = strip_tags(html_email)
        from_email = DEFAULT_FROM_EMAIL
        recipient_list = [issue.reported_by]
        email = EmailMultiAlternatives(subject, plain_text, from_email, recipient_list)
        email.attach_alternative(html_email, "text/html")
        email.send()

    except Exception as e:
        logger.error(
            f"Failed to send a resolved email for issue: {issue.title} with error: {e}",
            exc_info=True,
        )
