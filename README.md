source
======

Source is a website [dedicated to][sinker-explain] "advocating for, shining a spotlight on, and helping to generate community around the code that's being written in journalism." It's built with [Django][django], using Mozilla's [Playdoh web app template][gh-playdoh].

[sinker-explain]: http://sinker.tumblr.com/post/12203160394/journalism-in-the-open-hard-coding-community
[django]: http://www.djangoproject.com/
[gh-playdoh]: https://github.com/mozilla/playdoh


Installation
------------

### Requirements

You need Python 2.6 or 2.7, Mozilla's [funfactory][funfactory], MySQL, git, virtualenv, and a Unix-like OS.

[funfactory]: https://github.com/mozilla/funfactory

### Setup

First, make sure you've got funfactory installed, because the Playdoh app template will need it.

`pip install funfactory`

Then:

1. Fork and/or clone this Source repository from GitHub
2. Set up a virtual environment for your new project
3. Activate your virtualenv and cd into the project directory
4. Fetch the submodule dependancies

`git submodule update --init --recursive`

5. Make sure you have all the development requirements

`pip install -r requirements/dev.txt`

### Configuration

The existing database config points to sqlite for quick testing. If you'd rather switch to MySQL, you'll need to create a new database, adjust the DATABASES dict in source/settings/local.py accordingly, and then

`python manage.py syncdb`

This repository includes a few fixtures with test articles, people, organizations and code records for you to play with. If you'd like to add them, next run

`python manage.py loaddata test_data`

And then it's time to fire it up!

`python manage.py runserver`

Now you should be able view your dev server at [http://localhost:8000/][localhost]

[localhost]: http://localhost:8000/
