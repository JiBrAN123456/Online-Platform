# users/tasks.py
from celery import shared_task

@shared_task
def send_welcome_email(user_id):
    # Add your email sending logic here
    print(f"Sending welcome email to user {user_id}")
