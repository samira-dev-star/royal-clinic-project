from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Sliders,IndexIntroduction
import os


@receiver(post_delete, sender=Sliders)
def delete_slider_image(sender, instance, **kwargs):
    if instance.image_name:
        instance.image_name.close()
        image_path = instance.image_name.path
        if os.path.isfile(image_path):
            os.remove(image_path)
            
  
@receiver(post_delete, sender=IndexIntroduction)          
def delete_index_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.close()
        image_path = instance.image_name.path
        if os.path.isfile(image_path):
            os.remove(image_path)