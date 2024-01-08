import sentry_sdk
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email_validator import validate_email, EmailNotValidError

from emailing.models import Mail
from operators.models import Operator


def send_email_service(subject, client, link, sender=None):
    subject_for_client, message = get_subject_and_message(subject=subject, sender=sender, client=client, link=link)
    try:
        send_mail(subject=subject_for_client, message=strip_tags(message), recipient_list=get_recipient_list(client),
                  from_email=settings.EMAIL_HOST_USER, html_message=message)
        sent = True
    except:
        sentry_sdk.capture_message(f"E-mail sending was unsuccessfully {client} - {subject}")
        sent = False
    Mail.objects.create(
        client=client,
        subject=subject,
        sender=sender,
        message=strip_tags(message),
        sent=sent,
    )


def get_recipient_list(client):
    recipient_list = []
    for recipient in client.email.split(","):
        try:
            email = validate_email(recipient, check_deliverability=True)
            recipient_list.append(email.normalized)
        except EmailNotValidError:
            sentry_sdk.capture_message(f"{recipient} is not valid e-mail or not deliverable.")
    return recipient_list


def get_subject_and_message(link, client, subject, sender=None):
    context = {
        "operator": Operator.objects.get(),
        "sender": sender,
        "code": str(client.sign_code),
        "link": "http://" + link + "/clients/" + str(client.sign_code),
    }

    if "new" in subject:
        prefix = "Čeká na Vás nový dokument "
        template = "emailing/message_templates/new_document.html"
    elif "signed" in subject:
        prefix = "Podepsaný dokument "
        template = "emailing/message_templates/signed_document.html"
    elif "resend" in subject:
        prefix = "Odkaz k dokumentům v Samosetu pro klienta "
        suffix = client.name
        template = "emailing/message_templates/resend.html"

    if "proposal" in subject:
        suffix = f"Nabídka č. {subject.split(' ')[1]}"
    elif "contract" in subject:
        suffix = f"Smlouva č. {subject.split(' ')[1]}"
    elif "protocol" in subject:
        suffix = f"Předávací protokol ke smlouvě č. {subject.split(' ')[1]}"

    context["document"] = suffix

    message = render_to_string(template_name=template, context=context)
    subject = prefix + suffix

    return subject, message
