from django import forms


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='Upload a 28x28 pixel-intensity CSV',
        help_text='No header row. Values may be 0-255 or 0-1 — scaling is auto-detected.',
    )
