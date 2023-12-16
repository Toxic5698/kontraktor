from django import forms

from attachments.models import Attachment


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class AttachmentUploadForm(forms.ModelForm):
    file = MultipleFileField(required=True, label="Vyberte soubor")
    tag = forms.FileField(required=False, label="Označení souboru",
                          widget=forms.TextInput(attrs={"placeholder": "např. Zaměření ze dne..."}))

    class Meta:
        model = Attachment
        fields = ("tag", "file")
