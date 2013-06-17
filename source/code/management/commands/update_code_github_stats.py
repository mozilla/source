'''
Uses the GitHub API to update stats for Code repos.
'''
from datetime import datetime
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from source.code.models import Code

logging.basicConfig(filename='github_code_update.log', filemode='w', level=logging.INFO)

class Command(BaseCommand):
    help = 'Uses GitHub API to update stats for Code records.'
    def handle(self, *args, **options):
        logging.info('Started update: %s' % datetime.now())
        # get all the Code records with that have GitHub repos
        code_list = Code.objects.filter(url__icontains='//github.com/')
        
        for code in code_list:
            # attempt to fetch stats from GitHub API
            updated = code.update_github_stats()

            # save stats to database or log the error
            if updated:
                code.save()
                logging.info('Succesful update: %s' % code.name)
            else:
                logging.info('ERROR: %s' % code.name)

        logging.info('Finished update: %s' % datetime.now())
        
