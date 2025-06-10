from rest_framework import serializers
from .models import WaitlistUser, Referral, Reward

class WaitlistUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = WaitlistUser
        fields = ['email']


class StatsSerializer(serializers.Serializer):
    is_waitlist_active = serializers.BooleanField(default=True)
    waitlist_members = serializers.IntegerField()
    total_rewards = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_invites = serializers.IntegerField()
    total_members = serializers.IntegerField(required=False)
    countries = serializers.IntegerField(required=False)
    properties = serializers.IntegerField(required=False)