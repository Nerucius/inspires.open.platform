from django import shortcuts

from django.conf import settings

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext as _

from backend.models import User
from django.db.models import Model

import json


def create_wawp_link(email_name, context):
    """ Create a WAWP link for the given mail name and context """
    wawp_context = dict(**context)

    # Convert model instances to ID references
    for key, value in wawp_context.items():
        if isinstance(value, Model):
            wawp_context[key] = value.id

    wawp_link = settings.BACKEND_URL
    wawp_link = wawp_link + shortcuts.reverse("email_preview")
    wawp_link = wawp_link + "?email_name=%s&q=%s" % (
        email_name,
        json.dumps(wawp_context),
    )

    return wawp_link


def email_new_structure(structure):
    if not settings.EMAIL_HOST:
        return

    email_from = settings.EMAIL_FROM
    admins = User.objects.filter(groups__name="Administration").all()
    admin_emails = map(lambda x: x.email, admins)

    subject = _("Validate new Structure created by %(name)s") % (
        {"name": structure.created_by.full_name}
    )

    cta_link = settings.FRONTEND_URL
    cta_link = cta_link + "/administration"

    context = {"structure": structure, "cta_link": cta_link}
    wawp_link = create_wawp_link("email/new_structure.html", context)
    context["wawp_link"] = wawp_link

    html_message = render_to_string("email/new_structure.html", context)
    plain_message = strip_tags(html_message)

    mail.send_mail(
        subject, plain_message, email_from, admin_emails, html_message=html_message
    )


def email_new_evaluation(evaluation):
    if not settings.EMAIL_HOST:
        return

    email_from = settings.EMAIL_FROM
    email_to = evaluation.participation.user.email

    if not email_to:
        return

    subject = _("Evaluation questionnaire ready for %(project)s") % (
        {"project": evaluation.phase.project}
    )

    cta_link = settings.FRONTEND_URL
    cta_link = cta_link + "/evaluation/%d/entry" % evaluation.id

    context = {
        "evaluation": evaluation,
        "user": evaluation.participation.user,
        "cta_link": cta_link,
    }
    wawp_link = create_wawp_link("email/new_evaluation.html", context)
    context["wawp_link"] = wawp_link

    html_message = render_to_string("email/new_evaluation.html", context=context)
    plain_message = strip_tags(html_message)

    mail.send_mail(
        subject, plain_message, email_from, [email_to], html_message=html_message
    )

