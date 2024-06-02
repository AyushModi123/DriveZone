from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from base.permissions import IsInstructorPermission, IsLearnerPermission, RequiredProfileCompletionPermission
from base.models import User, ProfileCompletionLevelChoices
from slot.models import Slot
from .serializers import SlotSerializer, SemiSlotSerializer

@api_view(['POST'])
@permission_classes([IsInstructorPermission, RequiredProfileCompletionPermission(required_level=ProfileCompletionLevelChoices.COMPLETE)])
def create_slot(request):
    serializer = SlotSerializer(data=request.data)
    if serializer.is_valid():
        slot = serializer.save()
        return Response({
            'slot_start': serializer.data.get('slot_start'),
            'duration': serializer.data.get('duration')
        }, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_slots(request):
    current_user = request.user
    instructor_username = request.GET.get('username', None)
    if instructor_username:
        try:
            user = User.objects.get(username=instructor_username, instructor__isnull=False)
        except User.DoesNotExist:
            return Response('Instructor Not Found', status=404)        
        if current_user.is_learner:
            #Send Only Un-booked slots
            available_slots = Slot.objects.filter(instructor=user.instructor, is_booked=False)
            return Response({
                'slots': SlotSerializer(available_slots, many=True).data
                }
            )
        elif current_user.is_instructor:
            all_slots = Slot.objects.filter(instructor=user.instructor)
            return Response({
                'slots': SemiSlotSerializer(all_slots, many=True).data
                }
            )
        else:
            pass
    return Response('Instructor Not Found', status=404)
