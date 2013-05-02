'''
This management command updates Twitter information on a per-person basis,
one API call at a time. Ideally we'll never have to use this, and we'll
go with `bulk_update_twitter_bios` instead. This left here just in case.
'''
import twitter
from time import sleep

from django.conf import settings
from django.core.management.base import BaseCommand

from source.people.models import Person

# Twitter API 1.1 rate limit is 180 requests per 15-minute window
SLEEP_SECONDS = 6

class Command(BaseCommand):
    help = 'Uses Twitter 1.1 API to update bios and profile images for Person records.'
    def handle(self, *args, **options):
        api = twitter.Api(
            consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET,
            access_token_key=settings.TWITTER_ACCESS_TOKEN,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET
        )
        
        people = Person.objects.exclude(twitter_username='')
        for person in people:
            try:
                sleep(SLEEP_SECONDS)
                user = api.GetUser(person.twitter_username)
                person.twitter_bio = user.description
                person.twitter_profile_image_url = user.profile_image_url
                person.save()
            except twitter.TwitterError:
                # bad twitter username, don't update
                pass
            