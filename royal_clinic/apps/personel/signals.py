from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Personel
import os 




@receiver(post_delete, sender=Personel)
def delete_personel_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.close()
        image_path = instance.image.path
        if os.path.isfile(image_path):
            os.remove(image_path)