from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import ServiceVideo
import os


# instance denotates the record which is under action.
@receiver(post_delete, sender=ServiceVideo)
def delete_service_video(sender, instance, **kwargs):
    if hasattr(instance.video_file, 'close'):
        instance.video_file.close()
    file_path = instance.video_file.path
    if os.path.isfile(file_path):
        os.remove(file_path)
    
@receiver(post_delete, sender=ServiceVideo)    
def delete_service_thumbnail(sender, instance, **kwargs):
    if instance.thumbnail:
        instance.thumbnail.close()
        thumb_path = instance.thumbnail.path
        if os.path.isfile(thumb_path):
            os.remove(thumb_path)