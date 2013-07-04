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
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        
class PersonUpdateForm(ModelForm):
    class Meta:
        model = Person
        fields = (
            'first_name',
            'last_name',
            'email',
            'twitter_username',
            'github_username',
            'description',
        )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
