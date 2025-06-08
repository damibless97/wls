from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import WaitlistUser
from .serializers import WaitlistUserSerializer

@api_view(['POST'])
def join_waitlist(request):
    email = request.data.get('email')
    referred_by = request.data.get('referralCode')

    if WaitlistUser.objects.filter(email=email).exists():
        return Response({'message': 'Email already registered'}, status=400)

    user = WaitlistUser.objects.create(email=email, referred_by=referred_by)
    serializer = WaitlistUserSerializer(user)
    return Response(serializer.data)
