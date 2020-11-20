from django import forms

class FileFieldForm(forms.Form):
    name_field = forms.CharField(label = "Enter name", max_length =50)
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
