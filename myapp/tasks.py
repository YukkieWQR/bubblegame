# tasks.py

from celery import shared_task
from django.utils import timezone
from .models import UserProfile

@shared_task
def deactivate_turbo_task(user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
        if timezone.now() >= user.turbo_expiry:
            user.deactivate_turbo()
    except UserProfile.DoesNotExist:
        pass
