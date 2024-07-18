import logging
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from datetime import timedelta
from slot.constants import DEFAULT_SLOT_BACKWARD_QUERY_LIMIT, DEFAULT_SLOT_FORWARD_QUERY_LIMIT, DEFAULT_SLOT_FORWARD_LEARNER_QUERY_LIMIT
from project_cemphris.permissions import IsSchoolPermission, IsLearnerPermission, RequiredProfileCompletionPermission, BlockLearnerPermission
from base.models import Instructor
from slot.models import Slot
from course.models import EnrollCourse
from .serializers import SlotSerializer, OutSlotSerializer, OutShortSlotSerializer


logger = logging.getLogger(__file__)

@swagger_auto_schema()
class SlotView(APIView):

    def get_permissions(self):
        permission_classes =[BlockLearnerPermission, RequiredProfileCompletionPermission(required_level=50)]
        if self.request.method not in ('GET',):
            permission_classes+=[IsSchoolPermission]
        return [permission() for permission in permission_classes]

    @method_decorator(cache_page(settings.CACHE_TTL))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request):
        current_user = request.user
        blimit = request.GET.get("blimit", DEFAULT_SLOT_BACKWARD_QUERY_LIMIT)
        flimit = request.GET.get("flimit", DEFAULT_SLOT_FORWARD_QUERY_LIMIT)
        try:
            blimit = int(blimit)
        except (TypeError, ValueError):
            logger.info(f"Invalid blimit. Setting blimit to default {DEFAULT_SLOT_BACKWARD_QUERY_LIMIT}")
            blimit = DEFAULT_SLOT_BACKWARD_QUERY_LIMIT
        try:
            flimit = int(flimit)
        except (TypeError, ValueError):
            logger.info(f"Invalid flimit. Setting flimit to default {DEFAULT_SLOT_FORWARD_QUERY_LIMIT}")
            flimit = DEFAULT_SLOT_FORWARD_QUERY_LIMIT

        if current_user.is_school:
            q = request.GET.get("q", "")
            slots = Slot.objects.filter(
                Q(school=current_user.school) &
                Q(start_time__gte=timezone.now()-timedelta(days=blimit)) &
                Q(start_time__lte=timezone.now()+timedelta(days=flimit)) &
                (
                    Q(instructor__full_name__icontains=q)
                )
            )
            return Response({'slots': OutSlotSerializer(slots, many=True).data}, status=200)
        elif current_user.is_instructor:
            slots = Slot.objects.filter(
                Q(instructor=current_user.instructor) &
                Q(start_time__gte=timezone.now()-timedelta(days=blimit)) &
                Q(start_time__lte=timezone.now()+timedelta(days=flimit))
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

@cache_page(settings.CACHE_TTL)
@vary_on_headers("Authorization")
@swagger_auto_schema(
    method='GET',
)
@api_view(['GET'])
@permission_classes([IsLearnerPermission, RequiredProfileCompletionPermission(required_level=100)])
def get_available_instructor_slots(request):
    current_user = request.user

    # Validate queried id
    inst_id = request.GET.get("id")
    try:
        inst_id = int(inst_id)
    except (TypeError, ValueError):
        logger.info(f"Invalid instructor id")
        return Response({"error": "Invalid instructor id"}, status=400)

    # Check if instructor with queried id exists
    try:
        instructor = Instructor.objects.get(pk=inst_id)
    except Instructor.DoesNotExist:
        logger.info(f"Instructor not found")
        return Response({"message": "Not Found"}, status=404)

    # Check if learner is enrolled with this instructor
    try:
        enroll_course = EnrollCourse.objects.get(
                instructor=instructor,
                learner=current_user
                )
    except EnrollCourse.DoesNotExist:
        logger.info(f"Instructor with queried learner not found")
        return Response({"message": "Not Found"}, status=404)

    # Filter Available Slots
    slots = Slot.objects.filter(
                Q(instructor=instructor) &
                Q(is_booked=False) &
                Q(start_time__lte=timezone.now()+timedelta(days=DEFAULT_SLOT_FORWARD_LEARNER_QUERY_LIMIT))
            )
    return Response({'slots': OutShortSlotSerializer(slots, many=True).data}, status=200)
