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
4. Make sure you have all the development requirements

`pip install -r /requirements/dev.txt`

### Configuration

This repository includes a sqlite demo database, with a few articles, people, organizations and code pages in place for you to play with. If you want to switch over to MySQL instead, you'll need to create a new database, adjust the DATABASES dict in source/settings/local.py accordingly, and then

`manage.py syncdb`

Or just leave things pointing to the sqlite demo database for a quick peek. Either way, it's time to fire it up!

`manage.py runserver`

And you should be able view your dev server at [http://localhost:8000/][localhost]

[localhost]: http://localhost:8000/
