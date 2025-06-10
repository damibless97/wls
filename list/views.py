from rest_framework.response import Response
from .models import WaitlistUser, Referral, Reward
from .serializers import WaitlistUserSerializer, StatsSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.db.models import Count, Sum
import random  # For demo purposes - replace with real data

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
# def join_waitlist(request):
#     try:
#         email = request.data.get('email')
#         ref = request.data.get('ref')
        
#         if not email:
#             return Response({'error': 'Email is required'}, status=400)

#         if WaitlistUser.objects.filter(email=email).exists():
#             return Response({'message': 'Email already registered'}, status=400)

#         user = WaitlistUser.objects.create(email=email)
#         serializer = WaitlistUserSerializer(user)
#         return Response(serializer.data)

#     except Exception as e:
#         print("Error in join_waitlist:", str(e))
#         traceback.print_exc()
#         return Response({'error': str(e)}, status=500)

def join_waitlist(request):
    email = request.data.get('email')
    ref = request.data.get('ref')  # this is the referrer's email

    if WaitlistUser.objects.filter(email=email).exists():
        return Response({'message': 'Email already registered'}, status=400)

    user = WaitlistUser.objects.create(email=email)
    Reward.objects.create(user=user, joined_reward=10)

    # Save referral if ref email is valid
    if ref:
        try:
            referrer = WaitlistUser.objects.get(email=ref)
            Referral.objects.create(referrer=referrer, referred_email=email)

            reward, created = Reward.objects.get_or_create(user=referrer)
            reward.referral_reward += 5  # Give 5 ODAN per referral
            reward.save()

        except WaitlistUser.DoesNotExist:
            pass  # ignore if the referrer doesn't exist

    return Response({'message': 'Successfully joined waitlist'})



@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_stats(request):
    # Calculate basic stats
    waitlist_members = WaitlistUser.objects.count()
    total_rewards = Reward.objects.aggregate(
        total=Sum('joined_reward') + Sum('referral_reward')
    )['total'] or 0
    total_invites = Referral.objects.count()
    
    # For demo - replace with your actual logic to determine waitlist status
    is_waitlist_active = True  # Change this based on your business logic
    
    data = {
        'is_waitlist_active': is_waitlist_active,
        'waitlist_members': waitlist_members,
        'total_rewards': total_rewards,
        'total_invites': total_invites,
    }
    
    if not is_waitlist_active:
        # Add post-waitlist stats (replace with real data)
        data.update({
            'total_members': waitlist_members + random.randint(5000, 10000),
            'countries': random.randint(30, 80),
            'properties': random.randint(10, 50),
        })
    
    serializer = StatsSerializer(data)
    return Response(serializer.data)

from django.http import JsonResponse
from django.contrib.auth import get_user_model

def create_superuser(request):
    User = get_user_model()
    if not User.objects.filter(username="forext").exists():
        User.objects.create_superuser("forext", "odanforext@gmail.com", "Akin4forext")
        return JsonResponse({"status": "created"})
    return JsonResponse({"status": "already exists"})




