from datetime import timedelta

from django.conf import settings
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils import timezone
from django.views.generic import DetailView, View
from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse

from base.methods import get_model, get_document_through_class_id, get_data_in_dict, compare_text
from documents.models import DocumentSection, DocumentParagraph
from operators.models import Operator


class DocumentView(DetailView):

    def get_queryset(self):
        document_type = self.kwargs["document_type"]
        model = get_model(model_name=document_type)
        queryset = model.objects.filter(pk=self.kwargs["pk"])
        return queryset

    def get_template_names(self):
        template = f"{self.kwargs['document_type'] + 's'}/{self.kwargs['document_type']}_mustr.html"
        return [
            template,
        ]

    def get_context_data(self, **kwargs):
        document = self.get_queryset().get()

        context = {
            "operator": Operator.objects.get(),
        }
        if "edit-view" in self.request.META["PATH_INFO"]:
            context["edit_mode"] = True
        else:
            context["edit_mode"] = False
        if document.client.signatures.exists() and document.signed_at:
            context["signature"] = document.client.signatures.all().last()  # TODO: spárovat podpis k dokumentu
        paragraphs = document.paragraphs.all().order_by("priority")
        context["paragraphs"] = paragraphs
        attachments = document.get_document_attachments()
        if len(attachments) > 0:
            context["attachments"] = attachments

        if self.kwargs["document_type"] == "contract":
            context["contract"] = document
            context["proposal"] = document.proposal
            sections = {}
            for section in (
                    DocumentSection.objects.filter(document_paragraphs__in=paragraphs).distinct().order_by("priority")
            ):
                sections[section.name] = paragraphs.filter(document_section=section).values("id", "text", "editable")
            context["sections"] = sections

        if self.kwargs["document_type"] == "proposal":
            context["proposal"] = document
            context["proposal_validity"] = document.edited_at + timedelta(days=Operator.objects.get().proposal_validity)
            context["production_data"] = document.items.filter(production_data__isnull=False)

        if self.kwargs["document_type"] == "protocol":
            context["protocol"] = document
            context["proposal"] = document.contract.proposal

        return context


class PrintView(WeasyTemplateResponseMixin, DocumentView):
    pdf_stylesheets = [
        settings.PDF_STYLE,
        settings.PDF_FONT,
    ]
    pdf_attachment = True
    response_class = WeasyTemplateResponse


class DownloadView(WeasyTemplateResponseMixin, DocumentView):
    pdf_filename = f'Dokument ze SAMOSETu {timezone.now().strftime("%d.%m.%Y")}.pdf'


class DocumentParagraphView(View):

    def get(self, request, document_class_id, *args, **kwargs):
        document = get_document_through_class_id(document_class_id)
        context = {"document": document}
        return TemplateResponse(request=request, template="documents/edit_paragraphs.html", context=context)


class EditParagraphView(View):

    def get(self, request, pk, *args, **kwargs):
        old_paragraph = DocumentParagraph.objects.get(id=pk)
        document = get_document_through_class_id(request.htmx.current_url.split("/")[-1].split("?")[0])
        context = {"paragraph": old_paragraph, "document": document}
        return TemplateResponse(request=request, template="documents/paragraphs_form.html", context=context)

    def post(self, request, pk, *args, **kwargs):
        old_paragraph = DocumentParagraph.objects.get(id=pk)
        data = get_data_in_dict(request)
        result = self.replace_paragraph(document=data.get("document"), old_paragraph=old_paragraph, text=data.get("new-text"))
        return result

    def replace_paragraph(self, document, old_paragraph, text):
        document = get_document_through_class_id(document)
        dupla = DocumentParagraph.objects.filter(text=text)
        if old_paragraph.default and not dupla.exists():
            new_paragraph = DocumentParagraph.objects.create(
                document_type=old_paragraph.document_type,
                document_section=old_paragraph.document_section,
                priority=old_paragraph.priority,
                text=text,
                essential=old_paragraph.essential,
                editable=old_paragraph.editable,
                default=False,
                parent_id=old_paragraph.id,
            )
            document.paragraphs.remove(old_paragraph)
            document.paragraphs.add(new_paragraph)
        elif dupla.exists():
            document.paragraphs.remove(old_paragraph)
            document.paragraphs.add(dupla.get())
        elif not old_paragraph.default and not dupla.exists():
            old_paragraph.text = text
            old_paragraph.save()
        else:
            return HttpResponse(f"<span class='text-danger' id='paragraph-saved'>Změnu se nepodařilo uložit.</span>")
        return HttpResponse(f"<span class='text-success' id='paragraph-saved'>Změna uložena.</span>")


def text_compare_view(request, pk):
    new_text = get_data_in_dict(request).get("new-text")
    old_text = DocumentParagraph.objects.get(id=pk).text
    compared_text = compare_text(old_text, new_text)
    return HttpResponse(compared_text)
