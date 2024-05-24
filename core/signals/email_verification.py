from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import AdminProfile
from core.tasks import send_verification_email_task

@receiver(post_save, sender=AdminProfile)
def verification_mail(sender, instance, created, **kwargs):
    if created:
        print(instance, "verification_mail")
        send_verification_email_task.delay(instance.id)
        

