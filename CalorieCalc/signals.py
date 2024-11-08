from django.db.models.signals import post_save,post_migrate
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Weight
from .views import food


User = get_user_model()

@receiver(post_save, sender=User)
def create_weight_instance(sender, instance, created, **kwargs):
    if created:
        Weight.objects.create(user=instance, weight=instance.weight, date=timezone.now().date())

