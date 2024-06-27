from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from base.permissions import IsSchoolPermission, IsLearnerPermission, RequiredProfileCompletionPermission, BlockLearnerPermission
from base.models import User, ProfileCompletionLevelChoices
from slot.models import Slot
from .serializers import SlotSerializer, OutSlotSerializer

@swagger_auto_schema()
class SlotView(APIView):

    def get_permissions(self):
        permission_classes =[BlockLearnerPermission, RequiredProfileCompletionPermission(required_level=50)]
        if self.request.method not in ('GET',):
            permission_classes+=[IsSchoolPermission]
        return [permission() for permission in permission_classes]

    def get(self, request):
        current_user = request.user
        if current_user.is_school:
            q = request.GET.get("q", "")
            slots = Slot.objects.filter(
                Q(school=current_user.school) &
                (
                    Q(instructor__full_name__icontains=q)              
                )
            )
            return Response({'slots': OutSlotSerializer(slots, many=True).data}, status=200)
        elif current_user.is_instructor:
            slots = Slot.objects.filter(
                instructor=current_user.instructor
            )
            return Response({'slots': OutSlotSerializer(slots, many=True).data}, status=200)
        else:
            return Response({"message": "Access Denied"}, status=403)
    @swagger_auto_schema(request_body=SlotSerializer)
    def post(self, request):
        current_user = request.user
        serializer = SlotSerializer(data=request.data)
        if serializer.is_valid():                        
            slot = serializer.save(                
                school=current_user.school
            )
            return Response({'message': 'Slot created', 'slot_id': slot.id}, status=201)
        else:
            return Response(serializer.errors, status=400)
