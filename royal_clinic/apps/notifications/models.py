from django.db import models
from apps.accounts.models import Customuser

# Create your models here.


from django.contrib.auth import get_user_model



class Notification(models.Model):
    recipient = models.ForeignKey(Customuser, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.recipient.name}: {self.message[:30]}"
    
    class Meta:
        verbose_name = 'اعلان'
        verbose_name_plural = 'اعلانات'
