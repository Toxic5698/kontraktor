from datetime import timedelta

from django.apps import apps
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.views.generic import DetailView

from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse

from attachments.serializers import attachments_serializer
from contracts.models import ContractSection
from operators.models import Operator


class DocumentView(DetailView):

    def get_queryset(self):
        model = get_document_model(self.kwargs["type"])
        queryset = model.objects.filter(pk=self.kwargs['pk'], client__sign_code=self.kwargs['sign_code'])
        return queryset

    def get_template_names(self):
        template = f"{self.kwargs['type'] + 's'}/{self.kwargs['type']}_mustr.html"
        return [template, ]

    def get_context_data(self, **kwargs):
        context = {
            "operator": Operator.objects.get(),
        }
        if self.kwargs["type"] == "contract":
            contract = self.get_queryset().get()
            context["contract"] = contract
            context["proposal"] = contract.proposal
            context["attachments"] = attachments_serializer(
                contract.client.attachments.filter_contracts()) + attachments_serializer(
                contract.client.default_attachments.filter_contracts())
            cores = contract.contract_cores.filter(Q(subject__isnull=True) | Q(subject=contract.proposal.subject))

            sections = {}
            for section in ContractSection.objects.filter(contract_cores__in=cores).distinct().order_by('priority'):
                sections[section.name] = cores.filter(contract_section=section).values_list("text", flat=True)
            context["sections"] = sections

            if contract.client.signatures.exists() and contract.signed_at:
                context["signature"] = contract.client.signatures.filter(contract=contract).last()

        if self.kwargs["type"] == "proposal":
            proposal = self.get_queryset().get()
            context["proposal"] = proposal
            context["proposal_validity"] = proposal.edited_at + timedelta(days=14)
            context["production_data"] = proposal.items.filter(production_data__isnull=False)
            context["attachments"] = attachments_serializer(
                proposal.client.attachments.filter_proposals()) + attachments_serializer(
                proposal.client.default_attachments.filter_contracts())

        if self.kwargs["type"] == "protocol":
            protocol = self.get_queryset().get()
            context["protocol"] = protocol
            context["proposal"] = protocol.contract.proposal
            context["attachments"] = attachments_serializer(
                protocol.client.attachments.filter_protocols()) + attachments_serializer(
                protocol.client.default_attachments.filter_protocols())

            if protocol.client.signatures.exists() and protocol.signed_at:
                context["signature"] = protocol.client.signatures.filter(protocol=protocol).last()

        return context


def get_document_model(doc_type):
    if doc_type == "proposal":
        app_label = "proposals"
    else:
        app_label = "contracts"
    model = apps.get_model(model_name=doc_type, app_label=app_label)
    return model


class PrintView(WeasyTemplateResponseMixin, DocumentView):
    pdf_stylesheets = [settings.PDF_STYLE,]
    pdf_attachment = True
    response_class = WeasyTemplateResponse


class DownloadView(WeasyTemplateResponseMixin, DocumentView):
    pdf_filename = f'Dokument ze SAMOSETu {timezone.now().strftime("%d.%m.%Y")}.pdf'

