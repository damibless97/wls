from rest_framework.response import Response
from .models import WaitlistUser
from .serializers import WaitlistUserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import logging
logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def join_waitlist(request):
    logger.info(f"HEADERS: {request.headers}")
    email = request.data.get('email')

    if WaitlistUser.objects.filter(email=email).exists():
        return Response({'message': 'Email already registered'}, status=400)

    user = WaitlistUser.objects.create(email=email)
    serializer = WaitlistUserSerializer(user)
    return Response(serializer.data)
