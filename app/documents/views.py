# views.py
import functools
import ssl

from django.conf import settings
from django.utils import timezone
from django.views.generic import DetailView

from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse
from django_weasyprint.utils import django_url_fetcher

from clients.views import DocumentView
from documents.models import Document
from proposals.models import Proposal


def custom_url_fetcher(url, *args, **kwargs):
    # rewrite requests for CDN URLs to file path in STATIC_ROOT to use local file
    cloud_storage_url = 'https://kontraktor.s3.amazonaws.com/static/'
    if not url.startswith(cloud_storage_url):
        url = 'file://' + url.replace(cloud_storage_url, settings.STATIC_URL)
    return django_url_fetcher(url, *args, **kwargs)


class CustomWeasyTemplateResponse(WeasyTemplateResponse):
    # customized response class to pass a kwarg to URL fetcher
    def get_url_fetcher(self):
        # disable host and certificate check
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return functools.partial(custom_url_fetcher, ssl_context=context)


class PrintView(WeasyTemplateResponseMixin, DocumentView):
    # output of MyDetailView rendered as PDF with hardcoded CSS
    pdf_stylesheets = [
        "https://kontraktor.s3.eu-north-1.amazonaws.com/static/css/styles.css",
    ]
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = True
    # custom response class to configure url-fetcher
    response_class = WeasyTemplateResponse


class DownloadView(WeasyTemplateResponseMixin, DocumentView):
    # suggested filename (is required for attachment/download!)
    pdf_filename = 'foo.pdf'


# class DynamicNameView(WeasyTemplateResponseMixin, MyDetailView):
#     # dynamically generate filename
#     def get_pdf_filename(self):
#         return 'foo-{at}.pdf'.format(
#             at=timezone.now().strftime('%Y%m%d-%H%M'),
#         )
