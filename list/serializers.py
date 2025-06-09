from rest_framework import serializers
from .models import WaitlistUser

class WaitlistUserSerializer(serializers.ModelSerializer):
    referrals_count = serializers.SerializerMethodField()

    class Meta:
        model = WaitlistUser
        fields = ['email']

