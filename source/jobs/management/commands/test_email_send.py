'''
Testing the Amazon email hookup.
'''
import logging
from datetime import datetime
from time import sleep

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from source.utils.email import send_multipart_email

logging.basicConfig(filename='email_job_reminders.log', filemode='w', level=logging.INFO)


class Command(BaseCommand):
    help = 'Testing email via Amazon SMTP.'
    def handle(self, *args, **options):
        logging.info('Started job: %s' % datetime.now())
        
        # add context for rendering personalized emails
        subject = '[Source] Testing email via Amazon SMTP'
        email_context = {}
        
        # render text and html versions of email body
        text_content = render_to_string(
            'jobs/emails/job_post_reminder.txt',
            email_context,
        )
        html_content = render_to_string(
            'jobs/emails/job_post_reminder.html',
            email_context
        )

        # send email to each recipient
        email_recipients = ['ryan.a.pitts@gmail.com', 'john.p.schneider@gmail.com']
        for recipient in email_recipients:
            send_multipart_email(
                subject = subject,
                from_email = settings.DEFAULT_FROM_EMAIL,
                to = recipient,
                text_content = text_content,
                html_content = html_content
            )
            
            # avoid rate limit
            sleep(1)
            
        
        logging.info('Finished job: %s' % datetime.now())

