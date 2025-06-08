from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import CustomPatient
import os

@receiver(post_delete, sender=CustomPatient)
def delete_custom_patient(sender, instance, **kwargs):
    if instance.image_name:
        instance.image_name.close()
        image_path = instance.image_name.path
        if os.path.isfile(image_path):
            os.remove(image_path)