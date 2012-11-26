from django import forms

class UploadFileForm(forms.Form):
    imagen  = forms.FileField()