from time import sleep
from celery import shared_task

@shared_task
def notify_customers(message):
    print('Sending emails to 10k users.')
    print(message)
    sleep(10)
    print('Completed.')
