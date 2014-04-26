from datetime import datetime, timedelta
from dateutil import parser

from django.conf import settings
from django.views.generic import View

from source.articles.models import Article
from source.utils.json import render_json_to_response

USER_DEBUG = getattr(settings, 'USER_DEBUG', False)


class ContributorCount(View):
    def get(self, request, *args, **kwargs):
        '''
        Returns the following counts for Mozilla contributors dashboard:
        
        * Distinct authors who published articles in the previous year
        * New authors who published articles in the previous week, where "new"
          means they have not published in the previous year
        * Distinct people associated with articles published in the previous year
        * New people associated with articles published in the previous week,
          where "new" means they have not been mentioned in the previous year
        
        These counts reflect the way Source articles can be associated
        with individuals:
        
        * Authors: The person or people who wrote the article
        * People: A person or people whose work is being covered by the article.
          These people may or may not also be listed as article Authors.
        
        A date may be passed as a querystring parameter to provide a starting
        point for calculations. If no date is passed, `today` will be assumed.
        
        * /api/1.0/contributor-count/
        * /api/1.0/contributor-count/?date=2014-04-12
        
        Date ranges will be calculated from midnight of the starting date, so
        records won't be missed based on the time of day when the query is run.
        '''
        
        # set up the date parameters
        requested_date = request.GET.get('date', None)
        if requested_date:
            start_date = parser.parse(requested_date)
        else:
            today = datetime.today()
            midnight = datetime.min.time()
            start_date = datetime.combine(today, midnight)
            
        previous_year = start_date - timedelta(days=365)
        previous_7_days = start_date - timedelta(days=7)
        
        # set up the necessary article querysets
        articles_year = Article.live_objects.filter(pubdate__lt=start_date, pubdate__gte=previous_year)
        articles_7_days = Article.live_objects.filter(pubdate__lt=start_date, pubdate__gte=previous_7_days)
        articles_year_exclude_7_days = Article.live_objects.filter(pubdate__lt=previous_7_days, pubdate__gte=previous_year)

        # get down to counting some authors
        # first, take all the articles published in the previous year, fetch
        # the pk values for their `authors` m2m relationship
        authors_previous_year = articles_year.values_list('authors', flat=True)
        # filter out `none` values, use set() to remove dupes, count members
        authors_previous_year_count = len(set(filter(None, authors_previous_year)))
        
        # repeat process for articles published in the previous week, but only
        # to the point where we're creating the set of unique author values
        authors_previous_7_days = articles_7_days.values_list('authors', flat=True)
        authors_previous_7_days_set = set(filter(None, authors_previous_7_days))
        
        # do the same for articles published during previous year but NOT
        # during the previous week
        authors_previous_year_exclude_7_days = articles_year_exclude_7_days.values_list('authors', flat=True)
        authors_previous_year_exclude_7_days_set = set(filter(None, authors_previous_year_exclude_7_days))
        
        # then use set difference to find author values from previous 7 days
        # that do NOT appear elsewhere in the previous year
        authors_new_previous_7_days_count = len(
            authors_previous_7_days_set.difference(authors_previous_year_exclude_7_days_set)
        )

        # now repeat all of that for people associated with published articles
        people_previous_year = articles_year.values_list('people', flat=True)
        people_previous_year_count = len(set(filter(None, people_previous_year)))

        people_previous_7_days = articles_7_days.values_list('people', flat=True)
        people_previous_7_days_set = set(filter(None, people_previous_7_days))
        
        people_previous_year_exclude_7_days = articles_year_exclude_7_days.values_list('people', flat=True)
        people_previous_year_exclude_7_days_set = set(filter(None, people_previous_year_exclude_7_days))
        
        people_new_previous_7_days_count = len(
            people_previous_7_days_set.difference(people_previous_year_exclude_7_days_set)
        )
        
        result = {
            'start_date': datetime.strftime(start_date, '%Y-%m-%d'),
            'previous_year': datetime.strftime(previous_year, '%Y-%m-%d'),
            'previous_7_days': datetime.strftime(previous_7_days, '%Y-%m-%d'),
            'authors_previous_year': authors_previous_year_count,
            'authors_new_previous_7_days': authors_new_previous_7_days_count,
            'people_previous_year': people_previous_year_count,
            'people_new_previous_7_days': people_new_previous_7_days_count
        }
        
        return render_json_to_response(result)
        