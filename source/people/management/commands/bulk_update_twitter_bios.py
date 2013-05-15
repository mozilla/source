'''
Uses the Twitter API bulk lookup to grab data for 100 users at at time.

Filters our Person records for those with Twitter usernames, breaks
that list into chunks of 100, then hits the Twitter lookup with each
chunk. Loops through the response and uses an .update() query to update
the `twitter_bio` and `twitter_profile_image_url` for each Person.
'''
from datetime import datetime
import json
import logging
import oauth2 as oauth
from time import sleep

from django.conf import settings
from django.core.management.base import BaseCommand

from source.people.models import Person

# Twitter API 1.1 rate limit is 180 requests per 15-minute window
SLEEP_SECONDS = 6

CONSUMER_KEY=settings.TWITTER_CONSUMER_KEY
CONSUMER_SECRET=settings.TWITTER_CONSUMER_SECRET
ACCESS_KEY=settings.TWITTER_ACCESS_TOKEN
ACCESS_SECRET=settings.TWITTER_ACCESS_TOKEN_SECRET

logging.basicConfig(filename='twitter_update.log', filemode='w', level=logging.INFO)


def chunks(object_list, chunk_size=100):
    for i in xrange(0, len(object_list), chunk_size):
        yield object_list[i:i+chunk_size]

class Command(BaseCommand):
    help = 'Uses Twitter 1.1 API to update bios and profile images for Person records.'
    def handle(self, *args, **options):
        logging.info('Started update: %s' % datetime.now())
        # get all the Person records with Twitter usernames
        person_queryset = Person.objects.exclude(twitter_username='').values_list('twitter_username')
        # flatten the list of tuples from values_list
        person_list = list(sum(person_queryset, ()))
        # break up into chunks for the Twitter API
        person_list_sets = list(chunks(person_list))
        
        # set up Twitter credentials for our API calls
        consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
        access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
        client = oauth.Client(consumer, access_token)
        api_endpoint = 'https://api.twitter.com/1.1/users/lookup.json'

        # loop through our queryset in chunks of 100
        for person_set in person_list_sets:
            # hit the API with list of usernames
            querystring = '?screen_name=%s' % ','.join(person_set)
            response, data = client.request('%s%s' % (api_endpoint, querystring))

            # loop through the Twitter API response
            users = json.loads(data)
            for user in users:
                try:
                    # take the data from each user returned...
                    twitter_username = user['screen_name']
                    twitter_avatar = user['profile_image_url_https']
                    twitter_bio = user['description'] or ''
                
                    # ... and update directly into the matching Person record
                    # iexact because Twitter may return a screen_name with caps
                    Person.objects.filter(twitter_username__iexact=twitter_username).update(
                        twitter_bio = twitter_bio,
                        twitter_profile_image_url = twitter_avatar
                    )
                    logging.info('Succesful update: %s' % twitter_username)
                except:
                    logging.info('ERROR: %s' % user['screen_name'])
                    pass

            # abide by rate limit
            sleep(SLEEP_SECONDS)
        logging.info('Finished update: %s' % datetime.now())
        
