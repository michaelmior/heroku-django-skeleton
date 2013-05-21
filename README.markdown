Introduction
==

This project is a simple skeleton to get you started with Django and Heroku.
It currently uses the stable release of Django 1.5.
The steps below should get you up and running quickly.

Installation
==

To get started, first install the [Heroku Toolbelt](https://toolbelt.heroku.com/).
This will provide access to the necessary command-line tools.

Prepare the virtualenv you'll be using with the following commands:

    virtualenv venv --distribute
    source venv/bin/activate
    pip install -r requirements.txt

Then copy `env.sample` to `.env`.
Foreman uses this file to set environment variables when running commands.
Create a new PostgreSQL database and set the access information.

Issue the following commands to create the database and apply any migrations (this uses [South](http://south.aeracode.org/)).

    foreman run python manage.py syncdb
    foreman run python manage.py migrate

You're now all set for local development, to start the development server, simply run

    foreman run python manage.py runserver

You can then access the local development server at [`http://localhost:8000/`](http://localhost:8000/).


Deployment
==

The project is already set up for easy deployment with Heroku.
To create a new instance, run `heroku bootstrap`.
This requires the [heroku.json](https://github.com/rainforestapp/heroku.json) plugin which can be installed via `heroku plugins:install git@github.com:rainforestapp/heroku.json.git`.
Note that you will be warned that your account will be charged for the addons installed.
While I make no guarantees, I have attempted to select only free addons which leave room to upgrade.
You are still responsible for verifying any fees associated with any addons which will be installed.

To maintain the security of your installation, Django's secret key must be set to a [random string](https://www.grc.com/passwords.htm).

    heroku config:add DJANGO_SECRET_KEY="<random string here>"

For the first deploy, and each new deploy, simply run `git push heroku master`.
Initially, and when the schema changes, run `syncdb` and `migrate`.

    heroku run python manage.py syncdb
    heroku run python manage.py migrate

You can view your new deployment in your browser via `heroku open`.
Static file serving will be broken as this requires an S3 account.
Create a bucket on S3 and add the configuration to your Heroku installation.

    heroku config:add AWS_ACCESS_KEY_ID="<AWS access key>"
    heroku config:add AWS_SECRET_ACCESS_KEY="<AWS secret>"
    heroku config:add AWS_STORAGE_BUCKET_NAME="<bucket name>"


You can manually run `collectstatic via

    heroku run python manage.py collectstatic --noinput

Optionally, to have `collectstatic` run automatically on every deploy, use

    heroku labs:enable user-env-compile


Dependency management
==

To add a new dependency to your project, simply install via `pip install` after activating the virtualenv.
To track newly installed packages, run `pip freeze -l > requirements.txt` to update the requirements file.

Background tasks
==
This project is ready to go with background jobs via [Celery](http://www.celeryproject.org/).
Just define a task as specified in [the documentation](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#defining-and-calling-tasks).

By default, no workers will be running. To start one, run the following command.
Note that you WILL be billed by Heroku for running this additional dyno.

    heroku ps:scale celery=1
