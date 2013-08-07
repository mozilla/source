from django.contrib.auth.models import User, Group

from .models import Organization

def create_organization_user(email):
    try:
        # only create a user if there's a matching organization
        matching_organization = Organization.objects.get(email__iexact=email)
        # assign them to an admin group for possible future use
        organization_admin_group, created = Group.objects.get_or_create(name='Organization Admins')
        if matching_organization:
            new_user = User.objects.create_user(email, email)
            new_user.groups.add(organization_admin_group)
            return new_user
    except:
        return False
