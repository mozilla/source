'''
Uses the GitHub API to update stats for Organization records.
'''
from datetime import datetime
import dateutil.parser
import logging
import requests

from django.conf import settings
from django.core.management.base import BaseCommand

from source.code.models import Code

CLIENT_ID=settings.GITHUB_CLIENT_ID
CLIENT_SECRET=settings.GITHUB_CLIENT_SECRET

logging.basicConfig(filename='github_code_update.log', filemode='w', level=logging.INFO)

class Command(BaseCommand):
    help = 'Uses GitHub API to update stats for Code records.'
    def handle(self, *args, **options):
        logging.info('Started update: %s' % datetime.now())
        # get all the Person records with Twitter usernames
        code_list = Code.objects.filter(url__icontains='//github.com/')
        
        for code in code_list:
            github_location = code.url.split('github.com/')[1]
            github_user, github_repo = github_location.split('/')
            github_api_url = 'https://api.github.com/repos/%s/%s?client_id=%s&client_secret=%s' % (
                github_user.lower(), github_repo.lower(),
                CLIENT_ID, CLIENT_SECRET
            )

            r = requests.get(github_api_url)
            data = r.json

            try:
                # handle GitHub API's ISO8601 timestamps
                last_push = data['pushed_at'].strip('Z')
                last_push = dateutil.parser.parse(last_push, fuzzy=True)
                code.repo_last_push = last_push
                # the rest of the API data
                code.repo_forks = data['forks']
                code.repo_watchers = data['watchers']
                code.repo_description = data['description']
                code.repo_master_branch = data['master_branch']
                code.save()
                logging.info('Succesful update: %s' % github_location)
            except:
                logging.info('ERROR: %s' % github_location)
                pass

        logging.info('Finished update: %s' % datetime.now())
        
