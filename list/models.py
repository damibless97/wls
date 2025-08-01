from django.db import models
from django.utils import timezone
from datetime import timedelta

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




class WaitlistConfig(models.Model):
    waitlist_start = models.DateTimeField(auto_now_add=True)
    waitlist_duration_weeks = models.PositiveSmallIntegerField(default=3)
    is_active = models.BooleanField(default=True)

    @property
    def time_remaining(self):
        end_date = self.waitlist_start + timedelta(weeks=self.waitlist_duration_weeks)
        return max(end_date - timezone.now(), timedelta(0))

    @property
    def should_display_waitlist_stats(self):
        return self.time_remaining.total_seconds() > 0

    def save(self, *args, **kwargs):
        self.is_active = self.should_display_waitlist_stats
        super().save(*args, **kwargs)