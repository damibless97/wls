from rest_framework.response import Response
from .models import WaitlistUser, Referral, Reward, WaitlistConfig
from .serializers import WaitlistUserSerializer, StatsSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.db.models import Count, Sum
import re
from rest_framework.response import Response

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

    if not email:
        return Response({'error': 'Email is required'}, status=400)

    # Validate email domain
    allowed_domains = ['gmail.com', 'yahoo.com']
    domain_match = re.match(r'.+@(.+)$', email)
    if not domain_match or domain_match.group(1).lower() not in allowed_domains:
        return Response({'error': 'Only Gmail and Yahoo email addresses are allowed'}, status=401)

    if WaitlistUser.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered'}, status=402)

    user = WaitlistUser.objects.create(email=email)
    Reward.objects.create(user=user, joined_reward=5)  # Give 5 ODAN for joining

    # Save referral if ref email is valid
    if ref:
        try:
            referrer = WaitlistUser.objects.get(email=ref)
            Referral.objects.create(referrer=referrer, referred_email=email)

            reward, _ = Reward.objects.get_or_create(user=referrer)
            reward.referral_reward += 1.5  # Give 1.5 ODAN per referral
            reward.save()

        except WaitlistUser.DoesNotExist:
            pass  # ignore if the referrer doesn't exist

    return Response({'message': 'Successfully joined waitlist'})


# def join_waitlist(request):
#     email = request.data.get('email')
#     ref = request.data.get('ref')  # this is the referrer's email

#     if not email:
#         return Response({'error': 'Email is required'}, status=400)

#     if WaitlistUser.objects.filter(email=email).exists():
#         return Response({'message': 'Email already registered'}, status=400)

#     user = WaitlistUser.objects.create(email=email)
#     Reward.objects.create(user=user, joined_reward=5)  # Give 5 ODAN for joining

#     # Save referral if ref email is valid
#     if ref:
#         try:
#             referrer = WaitlistUser.objects.get(email=ref)
#             Referral.objects.create(referrer=referrer, referred_email=email)

#             reward, created = Reward.objects.get_or_create(user=referrer)
#             reward.referral_reward += 1.5  # Give 1.5 ODAN per referral
#             reward.save()

#         except WaitlistUser.DoesNotExist:
#             pass  # ignore if the referrer doesn't exist

#     return Response({'message': 'Successfully joined waitlist'})



@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_stats(request):
    # Get or create waitlist config
    config, _ = WaitlistConfig.objects.get_or_create(pk=1)
    
    # Calculate basic stats
    waitlist_members = WaitlistUser.objects.count()
    total_rewards = Reward.objects.aggregate(
        total=Sum('joined_reward') + Sum('referral_reward')
    )['total'] or 0
    total_invites = Referral.objects.count()
    
    data = {
        'is_waitlist_active': config.is_active,
        'waitlist_members': waitlist_members,
        'total_rewards': float(total_rewards),  # Convert Decimal to float for JSON
        'total_invites': total_invites,
        'time_remaining': config.time_remaining.total_seconds(),
    }
    
    if not config.is_active:
        # Add post-waitlist stats (replace with real queries as needed)
        from django.db.models import Count
        countries = Referral.objects.values('referred_email').annotate(
            country_code=Count('country')  # You'll need to add country field to model
        ).count()
        
        data.update({
            'total_members': waitlist_members,
            'countries': countries or 50,  # Fallback if no country data
            # 'properties': Property.objects.count(),  # Add this model if needed
        })
    
    return Response(data)






