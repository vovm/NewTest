from django import forms


class DateWidget(forms.TextInput):
    class Media:
        js = (
            'js/calendar.js',
            'http://code.jquery.com/ui/1.11.4/jquery-ui.js',
        )
        css = {
            'all': ('http://code.jquery.com/ui/1.11.4/themes/smoothness'
                    '/jquery-ui.css',)
        }
