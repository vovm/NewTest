from django import forms
from imagekit.forms import ProcessedImageField
from imagekit.processors import ResizeToFill

from .widgets import MyOwnWidget
from .models import About


class EditPersonForm(forms.ModelForm):
    date = forms.DateField(widget=MyOwnWidget(attrs={'class':'datepicker'}))
    image = ProcessedImageField(spec_id='hello:about:image',
                                           processors=[ResizeToFill(200, 200)],
                                           format='JPEG',
                                           options={'quality': 90})

    class Meta:
        model = About
