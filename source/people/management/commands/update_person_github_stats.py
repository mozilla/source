'''
Uses the GitHub API bulk lookup to udpates stats for Person records.
'''
from datetime import datetime
import logging
import requests

from django.conf import settings
from django.core.management.base import BaseCommand

from source.people.models import Person

CLIENT_ID=settings.GITHUB_CLIENT_ID
CLIENT_SECRET=settings.GITHUB_CLIENT_SECRET

logging.basicConfig(filename='github_person_update.log', filemode='w', level=logging.INFO)

class Command(BaseCommand):
    help = 'Uses GitHub API to update stats for Person records.'
    def handle(self, *args, **options):
        logging.info('Started update: %s' % datetime.now())
        # get all the Person records with Twitter usernames
        person_list = Person.objects.exclude(github_username='')
        
        for person in person_list:
            github_username = person.github_username
            github_api_url = 'https://api.github.com/users/%s?client_id=%s&client_secret=%s' % (
                github_username, CLIENT_ID, CLIENT_SECRET
            )
            r = requests.get(github_api_url)
            data = r.json
            try:
                person.github_repos_num = data['public_repos']
                person.github_gists_num = data['public_gists']
                person.save()
                logging.info('Succesful update: %s' % github_username)
            except:
                logging.info('ERROR: %s' % github_username)
                pass

        logging.info('Finished update: %s' % datetime.now())
        
