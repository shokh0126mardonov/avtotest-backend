from django import forms
from .models import User

class MessageAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'surname', 'password']

    def clean_username(self):
        content = self.cleaned_data.get('username')
        if len(content) < 5  or  len(content) > 128:
            raise forms.ValidationError("Content must be at least 5 characters long.")
        return content