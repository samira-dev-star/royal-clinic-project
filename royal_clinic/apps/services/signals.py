from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Services
import os


@receiver(post_delete, sender=Services)
def delete_image(sender, instance, **kwargs):
    if instance.service_image:
        instance.service_image.close()
    image_path = instance.service_image.path
    if os.path.isfile(image_path):
        os.remove(instance.service_image.path)