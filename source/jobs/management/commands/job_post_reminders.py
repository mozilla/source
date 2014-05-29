'''
Testing the Amazon email hookup.
'''
import logging
from datetime import datetime
from time import sleep

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from source.jobs.models import Job
from source.people.models import Organization
from source.utils.email import send_multipart_email

logging.basicConfig(filename='email_job_reminders.log', filemode='w', level=logging.INFO)


class Command(BaseCommand):
    help = 'Testing email via Amazon SMTP.'
    def handle(self, *args, **options):
        logging.info('Started job: %s' % datetime.now())
        
        organizations_with_jobs_ids = set(Job.live_objects.values_list('organization', flat=True))
        organizations_with_jobs = Organization.objects.filter(id__in=organizations_with_jobs_ids)
        
        for organization in organizations_with_jobs:
            jobs = Job.live_objects.filter(organization=organization)
            
        
        
            # add context for rendering personalized emails
            subject = '[Source] Monthly update from Source Jobs'
            email_context = {
                'site_url': settings.BASE_SITE_URL,
                'organization': organization,
                'jobs': jobs,
            }
        
            # render text and html versions of email body
            text_content = render_to_string(
                'jobs/emails/job_post_reminder.txt',
                email_context,
            )
            html_content = render_to_string(
                'jobs/emails/job_post_reminder.html',
                email_context
            )

            send_multipart_email(
                subject = subject,
                from_email = settings.DEFAULT_FROM_EMAIL,
                to = organization.email,
                text_content = text_content,
                html_content = html_content
            )
            
            # avoid rate limit
            sleep(1)
            
        
        logging.info('Finished job: %s' % datetime.now())

