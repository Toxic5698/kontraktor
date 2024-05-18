from django.db.models import Manager, Q


class DocumentParagraphManager(Manager):
    def editable(self):
        return self.instance.paragraphs.filter(editable=True).order_by("document_section__priority", "priority")
