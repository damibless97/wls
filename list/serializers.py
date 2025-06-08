from rest_framework import serializers
from .models import WaitlistUser

class WaitlistUserSerializer(serializers.ModelSerializer):
    referrals_count = serializers.SerializerMethodField()

    class Meta:
        model = WaitlistUser
        fields = ['email', 'referral_code', 'referrals_count']

    def get_referrals_count(self, obj):
        return WaitlistUser.objects.filter(referred_by=obj.referral_code).count()

