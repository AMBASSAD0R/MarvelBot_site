from django import forms
from .models import Comics, Users


class ComicsForm(forms.ModelForm):
    class Meta:
        model = Comics
        fields = (
            'name',
            'file_id',
            'cover_id',
            'colpage_pdf',
            'count_views',
        )
        widgets = {
            'name': forms.TextInput,
            'file_id': forms.TextInput,
            'cover_id': forms.TextInput,
        }


class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = (
            'user_id',
            'type_user',
            'count_reads',
        )
        widgets = {
            'user_id': forms.TextInput,
            'type_user': forms.TextInput
        }
