from rest_framework.response import Response
from .models import WaitlistUser
from .serializers import WaitlistUserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import traceback

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def join_waitlist(request):
    try:
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=400)

        if WaitlistUser.objects.filter(email=email).exists():
            return Response({'message': 'Email already registered'}, status=400)

        user = WaitlistUser.objects.create(email=email)
        serializer = WaitlistUserSerializer(user)
        return Response(serializer.data)

    except Exception as e:
        print("Error in join_waitlist:", str(e))
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)
