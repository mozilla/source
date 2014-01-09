'''
Collects new job listings and posts them to Twitter. This should be run
via cron, probably on an hourly basis during normal daylight hours.

This task fetches any job record where:
- `is_live` is True
- the current time falls between `listing_start_date` and `listing_end_date`
- the `tweeted_at` timestamp is empty

As this task posts jobs to Twitter, it updates the record's `tweeted_at`
timestampe, so it won't get posted next time the job runs. This lets us
set up the cron however we like, and it will always get the latest batch
of jobs that haven't been tweeted yet.
'''
from datetime import datetime
import logging
import oauth2 as oauth

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse

from source.jobs.models import Job

CONSUMER_KEY=settings.TWITTER_CONSUMER_KEY
CONSUMER_SECRET=settings.TWITTER_CONSUMER_SECRET
ACCESS_KEY=settings.TWITTER_ACCESS_TOKEN
ACCESS_SECRET=settings.TWITTER_ACCESS_TOKEN_SECRET

logging.basicConfig(filename='twitter_job_posts.log', filemode='w', level=logging.INFO)


class Command(BaseCommand):
    help = 'Posts new job listings to Twitter.'
    def handle(self, *args, **options):
        logging.info('Started posting: %s' % datetime.now())
        
        # set up Twitter credentials for our API calls
        consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
        access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
        client = oauth.Client(consumer, access_token)
        api_endpoint = 'https://api.twitter.com/1.1/statuses/update.json'

        # get all the Job records that are live, within proper
        # time frame, but have not been posted to Twitter yet
        jobs = Job.live_objects.filter(tweeted_at=None)

        # loop through our queryset
        for job in jobs:
            try:
                # build the tweet
                job_url = job.url or ('%s%s' % (settings.BASE_SITE_URL, reverse('job_list')))
                tweet = "New job listing from %s: %s %s" % (job.organization.name, job.name, job_url)
                
                # TODO: actually post to Twitter
                print tweet
                
                # update `tweeted_at` timestamp
                job.tweeted_at = datetime.now()
                job.save()
                
                logging.info('Succesful update: %s' % tweet)
            except:
                logging.info('ERROR: %s' % job)
                pass

        logging.info('Finished posting: %s' % datetime.now())
