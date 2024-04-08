import sentry_sdk
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email_validator import validate_email, EmailNotValidError

from emailing.models import Mail
from operators.models import Operator


def send_email_service(context=None, document=None, link=None, client=None):
    # odeslání přes formulář
    if context:
        message = render_to_string(template_name="emailing/message_templates/new_document.html", context=context)
        mail = context["mail"]
    # odeslání automaticky po podpisu
    elif document and link:
        mail = Mail.objects.create(
            client=document.client,
            subject=f"Podepsaný dokument ze služby SAMOSET",
            receiver=document.client.email,
        )
        context = {
            "operator": Operator.objects.get(),
            "document_name": document.get_name(),
            "link": link,
        }
        message = render_to_string(template_name="emailing/message_templates/signed_document.html", context=context)
    # odeslání automaticky po zadání e-mailu
    elif link and client:
        mail = Mail.objects.create(
            client=client,
            subject=f"Dokumenty ze služby SAMOSET",
            receiver=client.email,
        )
        context = {
            "operator": Operator.objects.get(),
            "client": client,
            "link": link,
        }
        message = render_to_string(template_name="emailing/message_templates/resend.html", context=context)

    try:
        send_mail(
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=mail.receiver.split(","),
            subject=mail.subject,
            message=strip_tags(message),
            html_message=message,
        )
    except:
        sentry_sdk.capture_message(f"E-mail sending was unsuccessfully {mail}")
        mail.status = "nepodařilo se odeslat"
        mail.save()
        return mail
    mail.status = "odeslán"
    mail.save()
    return mail


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
