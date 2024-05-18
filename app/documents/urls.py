from django.urls import path
from documents.views import *

urlpatterns = [
    path("print/<str:sign_code>/<str:document_type>/<str:pk>", PrintView.as_view(), name="print-document"),
    path("download/<str:sign_code>/<str:document_type>/<str:pk>", DownloadView.as_view(), name="download-document"),
    path("edit-view/<str:document_type>/<str:pk>", DocumentView.as_view(), name="edit-view"),
    path("document-paragraphs/<str:document_class_id>", DocumentParagraphView.as_view(), name="document-paragraphs"),
    path("paragraph-form/<str:pk>", EditParagraphView.as_view(), name="paragraph-form"),
    path("save-paragraph-text/<str:pk>", EditParagraphView.as_view(), name="save-paragraph-text"),
    path("get-text-with-changes/<str:pk>", text_compare_view, name="get-text-with-changes"),
]
