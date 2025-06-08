from django.db import models
import uuid

def generate_unique_referral_code():
    from .models import WaitlistUser
    while True:
        code = uuid.uuid4().hex[:6]
        if not WaitlistUser.objects.filter(referral_code=code).exists():
            return code

class WaitlistUser(models.Model):
    email = models.EmailField(unique=True)
    referral_code = models.CharField(max_length=10, unique=True, default=generate_unique_referral_code)
    referred_by = models.CharField(max_length=10, null=True, blank=True)
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
