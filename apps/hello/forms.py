from django import forms
from imagekit.forms import ProcessedImageField
from imagekit.processors import ResizeToFill

from .widgets import DateWidget
from .models import About, AllRequest


class EditPersonForm(forms.ModelForm):
    date = forms.DateField(widget=DateWidget(attrs={'class': 'datepicker'}))
    image = ProcessedImageField(spec_id='hello:about:image',
                                processors=[ResizeToFill(200, 200)],
                                format='JPEG',
                                options={'quality': 90})

    class Meta:
        model = About


class EditRequestForm(forms.ModelForm):
    class Meta:
        model = AllRequest
        exclude = ('req', 'date', 'method', 'path')
