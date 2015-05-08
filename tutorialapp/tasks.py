from __future__ import absolute_import
from celery import shared_task

 # @shared_task decorator share tasks with all apps of project
@shared_task
def example(x, y): # example function
    print (x + y) # will print in Celery terminal
