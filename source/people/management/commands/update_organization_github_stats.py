'''
Uses the GitHub API to update stats for Organization records.
'''
from datetime import datetime
import logging
import requests

from django.conf import settings
from django.core.management.base import BaseCommand

from source.people.models import Organization

CLIENT_ID=settings.GITHUB_CLIENT_ID
CLIENT_SECRET=settings.GITHUB_CLIENT_SECRET

logging.basicConfig(filename='github_org_update.log', filemode='w', level=logging.INFO)

class Command(BaseCommand):
    help = 'Uses GitHub API to update stats for Organization records.'
    def handle(self, *args, **options):
        logging.info('Started update: %s' % datetime.now())
        # get all the Person records with Twitter usernames
        organization_list = Organization.objects.exclude(github_username='')
        
        for organization in organization_list:
            github_username = organization.github_username
            github_api_url = 'https://api.github.com/orgs/%s?client_id=%s&client_secret=%s' % (
                github_username.lower(), CLIENT_ID, CLIENT_SECRET
            )
            r = requests.get(github_api_url)
            data = r.json
            try:
                organization.github_repos_num = data['public_repos']
                organization.github_gists_num = data['public_gists']
                organization.save()
                logging.info('Succesful update: %s' % github_username)
            except:
                logging.info('ERROR: %s' % github_username)
                pass

        logging.info('Finished update: %s' % datetime.now())
        
