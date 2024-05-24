from celery import shared_task
from auth.utils import send_verification_mail
from core.models import AdminProfile

@shared_task
def send_verification_email_task(pk):
    admin_profile = AdminProfile.objects.get(id=pk)
    print(admin_profile, "send_verification_email_task")
    send_verification_mail(admin_profile)
