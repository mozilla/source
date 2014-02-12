from django import forms
from django.forms import ModelForm

from .models import Job

class JobUpdateForm(ModelForm):
    class Meta:
        model = Job
        fields = (
            'name',
            'description',
            'location',
            'url',
            'contact_name',
            'email',
            'listing_end_date',
        )
