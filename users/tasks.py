from django.core.mail import send_mail
from celery import shared_task
from pentest_portal import settings
from django.template.loader import render_to_string


@shared_task(bind=True)
def send_mail_func(self, email, current_site, uid, token):
    context = {
        "current_site": current_site,
        "uid": uid,
        "token": token
    }
    email_body = render_to_string('users/confirm_email.html', context)
    mail_subject = "Activation mail"
    send_mail(
        subject=mail_subject,
        message=email_body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email, ],
        fail_silently=True,
    )
    return {"status": True}
