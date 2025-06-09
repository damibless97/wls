from django.db import models
import uuid

# def generate_unique_referral_code():
#     from .models import WaitlistUser
#     while True:
#         code = uuid.uuid4().hex[:6]
#         if not WaitlistUser.objects.filter(referral_code=code).exists():
#             return code

class WaitlistUser(models.Model):
    email = models.EmailField(unique=True)
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
