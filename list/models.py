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


class Referral(models.Model):
    referrer = models.ForeignKey(WaitlistUser, on_delete=models.CASCADE, related_name='referrals')
    referred_email = models.EmailField()
    date_referred = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referrer.email} referred {self.referred_email}"





class Reward(models.Model):
    user = models.OneToOneField(WaitlistUser, on_delete=models.CASCADE)
    joined_reward = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    referral_reward = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def total_reward(self):
        return self.joined_reward + self.referral_reward

    def __str__(self):
        return f"Rewards for {self.user.email}"
