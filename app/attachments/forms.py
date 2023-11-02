from django import forms

from attachments.models import Attachment


class AttachmentUploadForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}), required=True,
                           label="Vyberte soubor")
    tag = forms.FileField(required=False, label="Označení souboru",
                          widget=forms.TextInput(attrs={"placeholder": "např. Zaměření ze dne..."}))

    class Meta:
        model = Attachment
        fields = ("tag", "file")
