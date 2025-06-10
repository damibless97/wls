from rest_framework.response import Response
from .models import WaitlistUser, Referral, Reward
from .serializers import WaitlistUserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import traceback

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


def create_superuser(request):
    from django.contrib.auth.models import User
    if not User.objects.filter(username='forext').exists():
        User.objects.create_superuser('admin', 'odanforext@gmail.com', 'forext4ever')
    return Response({'message': 'Superuser created if it did not exist'})