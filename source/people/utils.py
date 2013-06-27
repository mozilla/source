from django.contrib.auth.models import User

from .models import Organization

def create_organization_user(email):
    # only create a user if there's a matching organization
    try:
        matching_organization = Organization.objects.get(email=email)
        if matching_organization:
            return User.objects.create_user(email, email)
    except:
        return False
