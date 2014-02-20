from django.contrib.auth.models import User, Group

from .models import Organization, Person

def create_auth_user(email):
    new_user = None
    # seek matching organization for new user
    try:
        matching_organization = Organization.objects.get(email__iexact=email)
        organization_admin_group, created = Group.objects.get_or_create(name='Organization Admins')

        # find matching organization before creating user record so we don't have orphans
        new_user = User.objects.create_user(email, email)
        new_user.groups.add(organization_admin_group)
    except:
        pass
        
    return new_user
