from django import shortcuts

from django.conf import settings

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags, urlencode
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
    # Create final link using the reverse route and the query parameters, escaped using
    # Django utils to fix a bug with hashtags on the route
    wawp_link = (
        wawp_link
        + "?"
        + urlencode({"email_name": email_name, "q": json.dumps(wawp_context)})
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


def email_reset_password(user):
    if not settings.EMAIL_HOST:
        return

    email_from = settings.EMAIL_FROM

    subject = _("Reset the password for your account")

    cta_link = settings.FRONTEND_URL
    cta_link = cta_link + "/reset-password?token=" + user.reset_password_token

    context = {"user": user, "cta_link": cta_link}
    wawp_link = create_wawp_link("email/reset_password.html", context)
    context["wawp_link"] = wawp_link

    html_message = render_to_string("email/reset_password.html", context)
    plain_message = strip_tags(html_message)

    mail.send_mail(
        subject, plain_message, email_from, [user.email], html_message=html_message
    )


def email_new_collaboration(collaboration):
    if not settings.EMAIL_HOST:
        return

    email_from = settings.EMAIL_FROM
    email_template = "email/new_collaboration.html"

    manager_emails = map(lambda x: x.email, collaboration.project.managers.all())

    subject = _("New project registered to your structure: %(project_name)s") % (
        {"project_name": collaboration.project.name}
    )

    cta_link = settings.FRONTEND_URL
    cta_link = (
        cta_link + "/structures/%d/manage#projectsTab" % collaboration.structure.id
    )

    context = {"collaboration": collaboration, "cta_link": cta_link}
    wawp_link = create_wawp_link(email_template, context)
    context["wawp_link"] = wawp_link

    html_message = render_to_string(email_template, context)
    plain_message = strip_tags(html_message)

    mail.send_mail(
        subject, plain_message, email_from, manager_emails, html_message=html_message
    )


def email_collaboration_approved(collaboration):
    if not settings.EMAIL_HOST:
        return

    email_from = settings.EMAIL_FROM
    email_template = "email/collaboration_approved.html"

    email_to = collaboration.created_by.email

    subject = _('Your request has been approved to be part of "%(structure_name)s"') % (
        {"structure_name": collaboration.structure.name}
    )

    cta_link = settings.FRONTEND_URL
    cta_link = cta_link + "/projects/%d" % collaboration.project.id

    context = {
        "collaboration": collaboration,
        "cta_link": cta_link,
        "user": collaboration.created_by,
    }
    wawp_link = create_wawp_link(email_template, context)
    context["wawp_link"] = wawp_link

    html_message = render_to_string(email_template, context)
    plain_message = strip_tags(html_message)

    mail.send_mail(
        subject, plain_message, email_from, [email_to], html_message=html_message
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

