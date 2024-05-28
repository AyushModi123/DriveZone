from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Instructor


@api_view(['GET'])
def check_api(request):
    return Response("Working")