from django import forms
from YAMLDatabase.models import YAMLEntry,Filename

class yamlform(forms.ModelForm):

    class Meta:
        model = YAMLEntry
        fields = "__all__"

    host = forms.CharField(required=False)
    username = forms.CharField(required=False)
    password = forms.CharField(required=False)
    device_type = forms.CharField(required=False)


class fnameform(forms.ModelForm):

    class Meta:
        model = Filename
        fields = "__all__"