from django.conf import settings

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from backend.models import User


def email_new_structure(structure):

    admins = User.objects.filter(groups__name="Administration").all()
    admin_emails = map(lambda x: x.email, admins)

    email_from = settings.EMAIL_HOST_USER

    subject = "[InSPIRES] Validate new Structure created by %s" % (
        structure.created_by.full_name
    )

    html_message = render_to_string(
        "email/new_structure.html", {"structure": structure}
    )
    plain_message = strip_tags(html_message)

    mail.send_mail(
        subject, plain_message, email_from, admin_emails, html_message=html_message
    )

