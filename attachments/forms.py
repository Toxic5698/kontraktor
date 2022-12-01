from django import forms

from attachments.models import Attachment


class AttachmentUploadForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}), required=False)

    class Meta:
        model = Attachment
        fields = ("name", "file")
