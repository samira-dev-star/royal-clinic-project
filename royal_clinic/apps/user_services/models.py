# from django.db import models
# from django.conf import settings
# # Create your models here.

# class UserServiceInteraction(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     service = models.ForeignKey('services.Services', on_delete=models.CASCADE)
#     saved_at = models.DateTimeField(auto_now_add=True)
#     is_favorite = models.BooleanField(default=False)
#     has_registered = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.user} -> {self.service}"
