from datetime import timedelta

from django.apps import apps
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.views.generic import DetailView

from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse

from attachments.serializers import attachments_serializer
from documents.models import DocumentSection
# from contracts.models import ContractSection
from operators.models import Operator


class DocumentView(DetailView):

    def get_queryset(self):
        document_type = self.kwargs['type']
        model = apps.get_model(model_name=document_type, app_label=document_type + "s")
        queryset = model.objects.filter(pk=self.kwargs['pk'], client__sign_code=self.kwargs['sign_code'])
        return queryset

    def get_template_names(self):
        template = f"{self.kwargs['type'] + 's'}/{self.kwargs['type']}_mustr.html"
        return [template, ]

    def get_context_data(self, **kwargs):
        document = self.get_queryset().get()

        context = {
            "operator": Operator.objects.get(),
        }
        if document.client.signatures.exists() and document.signed_at:
            context["signature"] = document.client.signatures.all().last()  # TODO: spárovat podpis k dokumentu
        paragraphs = document.paragraphs.all().order_by("priority")
        context["paragraphs"] = paragraphs
        attachments = attachments_serializer(document.attachments.all()) + attachments_serializer(
            document.default_attachments.all())
        if len(attachments) > 0:
            context["attachments"] = attachments

        if self.kwargs["type"] == "contract":
            context["contract"] = document
            context["proposal"] = document.proposal
            sections = {}
            for section in DocumentSection.objects.filter(document_paragraphs__in=paragraphs).distinct().order_by(
                    'priority'):
                sections[section.name] = paragraphs.filter(document_section=section).values_list("text", flat=True)
            context["sections"] = sections

        if self.kwargs["type"] == "proposal":
            context["proposal"] = document
            context["proposal_validity"] = document.edited_at + timedelta(days=Operator.objects.get().proposal_validity)
            context["production_data"] = document.items.filter(production_data__isnull=False)

        if self.kwargs["type"] == "protocol":
            context["protocol"] = document
            context["proposal"] = document.contract.proposal

        return context


def get_document_model(doc_type):
    if doc_type == "proposal":
        app_label = "proposals"
    else:
        app_label = "contracts"
    model = apps.get_model(model_name=doc_type, app_label=app_label)
    return model


class PrintView(WeasyTemplateResponseMixin, DocumentView):
    pdf_stylesheets = [
        settings.PDF_STYLE,
        settings.PDF_FONT,
    ]
    pdf_attachment = True
    response_class = WeasyTemplateResponse


class DownloadView(WeasyTemplateResponseMixin, DocumentView):
    pdf_filename = f'Dokument ze SAMOSETu {timezone.now().strftime("%d.%m.%Y")}.pdf'
