from django import forms
from django.forms import ModelForm

from .models import Organization, Person

class OrganizationUpdateForm(ModelForm):
    class Meta:
        model = Organization
        fields = (
            'twitter_username',
            'github_username',
            'homepage',
            'description',
            'address',
            'city',
            'state',
        )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
        }