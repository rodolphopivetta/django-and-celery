# **Django + Celery Tutorial**


## Installing Everything


### Installing Virtualenv

```Virtualenv``` is a tool to create isolated Python environments.

[Virtualenv Docs](https://virtualenv.pypa.io/en/latest/)
```bash
# install virtualenv
pip install virtualenv

# create a virtual python environments
virtualenv venv_tutorial --no-site-packages
```


### Installing Django 1.8

[Django Docs](https://docs.djangoproject.com/en/1.8/)
```bash
# activate virtual python environments
souce venv_tutorial/bin/activate

# install django
pip install django

# deactivate virtual python environments 
deactivate
```


### Installing RabbitMQ

RabbitMQ is a message transport used to send and receive messages.
Celery can run on a single machine, on multiple machines, or even across data centers with this.

[RabbitMQ Docs](https://www.rabbitmq.com/documentation.html)
```bash
sudo apt-get install rabbitmq-server
```
When the command completes the broker is already running in the background, ready to move messages for you: ```Starting rabbitmq-server: SUCCESS```.


### Installing Celery 3.1

[Celery Docs](http://celery.readthedocs.org/en/latest/)
```bash
# reactivate virtual python environments
souce venv_tutorial/bin/activate

# installing celery and django celery app
pip install celery django-celery
```


## Starting Celery with Django

This tutorial will use the following names

> **Virtualenv environments:** venv_tutorial

> **Django project:** tutorial

> **Django app:** tutorialapp


### Creating Django Project and App

```bash
django-admin startproject tutorial
cd tutorial
./manage.py startapp tutorialapp
```

Add the app **tutorialapp** in *INSTALLED_APPS* settings.

**file:** *tutorial/settings.py*
```python
#...
INSTALLED_APPS = (
	#...
	'tutorialapp',
	#...
)
#...
```


### Configuring Celery on Project Django

After start project and app in Django:

**file:** *tutorial/settings.py*
```python
#...
INSTALLED_APPS = (
	#...
	'djcelery',
	'kombu.transport.django',
	#...
)
#...
```

---
Create a file called **celery.py** in same level of **settings.py**

**file:** *tutorial/celery.py*
```python
from __future__ import absolute_import
import os
from celery import Celery

# set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutorial.settings')

from django.conf import settings
# set the celery project object as app
app = Celery('tutorial')

# Using a string here means the worker will not have to pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
	CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
	CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler",
	BROKER_URL = 'django://',
)
```

---
On **\_\_init\_\_.py** file on same level of **settings.py**
**file:** *tutorial/\_\_init\_\_.py*
```python
from __future__ import absolute_import
# This will make sure the app is always imported when Django starts so that shared_task will use this app
from .celery import app as celery_app
```


### Making tasks

Create a file called **tasks.py** in app folder (same level of **views.py**, **models.py**, etc)

**file:** *tutorialapp/tasks.py*
```python
from __future__ import absolute_import
from celery import shared_task

 # @shared_task decorator share tasks with all apps of project
@shared_task
def example(x, y): # example function
	print (x + y) # will print in Celery terminal
```

The tree of all project will be like:
```bash
├── manage.py
├── tutorial
│   ├── __init__.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
└── tutorialapp
    ├── __init__.py
    ├── admin.py
    ├── models.py
    ├── tasks.py
    ├── tests.py
    └── views.py
```


---
##	Start Celery with Django

```bash
# migrate app to database (including djcelery)
./manage.py migrate
# sync database with djcelery
./manage.py syncdb
# start celery
./manage.py celery -A tutorial worker -B -l info
```


---
### Create Periodic Tasks

Start Django project to create tasks in admin page.

*In **manage.py** file level*
```bash
./manage runserver
```

Access: [Admin Project Page](http://127.0.0.1:8000/admin)

In **Djcelery** app, choice **Periodic tasks** and click on **add periodic task** buttom.

> Set a name to Task

> Choice a task (in this case, **tutorialapp.tasks.example**)

> Check **Enabled**

> Set a **Inverval** (In this case, every 10 seconds)

> On **Arguments** set: [2, 2]

> Save

If that's all right, the terminal where "Celery" was started will show the sum of arguments (*2 + 2 = 4*) every 10 seconds.
Its done!


---
# Schedules


### Interval

Interval set an interval (*really?*) to execute a task
For example:
> 
- every **x**:
 - microseconds
 - seconds
 - minutes
 - hours
 - days


### Crontab

Crontab set when the task will be executed

For example:

> 
 - crontab()
  - Execute every minute.
 - crontab(minute=0, hour=0)
  - Execute daily at midnight.
 - crontab(minute=0, hour='*/3')
  - Execute every three hours: midnight, 3am, 6am, 9am, noon, 3pm, 6pm, 9pm.
 - crontab(minute='*/15')
  - Execute every 15 minutes.


## Running Celery in Background (*as a daemon*)

```bash
# install supervisor to django app
pip install django-supervisor
```

In the **settings.py** file, add:
**file:** *tutorial/settings.py*
```python
#...
INSTALLED_APPS = (
	#...
	'djsupervisor',
	#...
)
#...
```

Create a file called **supervisord.conf** in same level of **manage.py**:

**file:** *supervisord.conf*
```
[program:webserver]
command={{ PYTHON }} {{ PROJECT_DIR }}/manage.py runserver --noreload

[program:celeryworker]
command={{ PYTHON }} {{ PROJECT_DIR }}/manage.py celery worker -l info

[program:celerybeat]
command={{ PYTHON }} {{ PROJECT_DIR }}/manage.py celery beat -l info
```

And to run the server on **background**, use:
```bash
./manage.py supervisor --daemonize
```

To **STOP** the server, use:
```bash
./manage.py supervisor shutdown
```

That's it.

---
*Created by **Rodolpho Pivetta Sabino** *
