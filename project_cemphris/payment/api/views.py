from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from project_cemphris.permissions import IsLearnerPermission
from payment.models import PaymentDetail
from .serializers import PaymentSerializer
from payment.choices import PaymentStatusTypeChoices

@swagger_auto_schema(
    method='post',
    request_body=PaymentSerializer,    
)
@api_view(['POST'])
@permission_classes([IsLearnerPermission])
def checkout(request):
    current_user = request.user
    try:
        payment = PaymentDetail.objects.get(learner=current_user.learner, status=PaymentStatusTypeChoices.COMPLETE)
        return Response({"error": "Only 1 Course Allowed"}, status=400)
    except PaymentDetail.DoesNotExist:
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save(learner=current_user.learner, status=PaymentStatusTypeChoices.COMPLETE)
            return Response({"message": "Payment Successful", "payment_id": payment.id}, status=200)
        return Response(serializer.errors, status=400)

# def get_status(request, session_id):
    # accept session id in url
    # check payment status
    # if pending then wait for a timeout else if completed or failed return