from django.contrib import admin
from .models import WaitlistUser, Referral, Reward

# Register your models here.
@admin.register(WaitlistUser)
class WaitlistUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'joined')

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referred_email', 'date_referred')

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('user', 'joined_reward', 'referral_reward', 'total_reward')
