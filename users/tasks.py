# from django.contrib.auth import get_user_model
from users.models import User
from django.core.mail import send_mail
from celery.decorators import task
from pentest_portal import settings
# import json

@task()
def send_mail_func(user_id):
    user = User.objects.filter(pk=user_id)

    # to_email = user.email
    # print("to_email", to_email)
    mail_subject = "Hi! Celery Testing"
    message = 'If you are there...please be there always.'
    # to_email = 'darshanthapa872@gmail.com'
    send_mail(
        subject=mail_subject,
        message=message, 
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=user,
        fail_silently=False,
    )
    return{"status":True}