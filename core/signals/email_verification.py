from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import AdminProfile
from auth.utils import send_verification_mail

@receiver(post_save, sender=AdminProfile)
def verification_mail(sender, instance, created, **kwargs):
    if created:
        send_verification_mail(instance)
        

