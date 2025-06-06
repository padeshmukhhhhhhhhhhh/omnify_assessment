from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from .models import FitnessClass, Booking
from .serializers import *
import pytz
import logging

logger = logging.getLogger(__name__)

class ClassListAPIView(APIView):
    def get(self, request):
        tz_name = request.query_params.get('tz', 'Asia/Kolkata')  # default IST
        logger.info(f"Class list requested with timezone: {tz_name}")
        try:
            user_tz = pytz.timezone(tz_name)
        except pytz.UnknownTimeZoneError:
            logger.warning(f"Invalid timezone received: {tz_name}")
            return Response({'error': 'Invalid timezone'}, status=status.HTTP_400_BAD_REQUEST)

        classes = FitnessClass.objects.filter(start_time__gte=now()).order_by('start_time')
        logger.info(f"Retrieved {classes.count()} classes from DB")

        data = []
        for c in classes:
            localized_time = c.start_time.astimezone(user_tz)
            data.append({
                'id': c.id,
                'name': c.name,
                'instructor': c.instructor,
                'start_time': localized_time.strftime('%Y-%m-%d %I:%M:%S %p'),
                'available_slots': c.available_slots,
            })

        return Response(data, status=status.HTTP_200_OK)


class BookClassAPIView(APIView):
    def post(self, request):
        class_id = request.data.get('class_id')
        client_name = request.data.get('client_name')
        client_email = request.data.get('client_email')

        logger.info(f"Booking request received: class_id={class_id}, client_name={client_name}, client_email={client_email}")

        if not all([class_id, client_name, client_email]):
            logger.warning("Booking request missing required fields")
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not str(class_id).isdigit():
            return Response({'error': 'Class ID must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

        class_id = int(class_id)


        try:
            fitness_class = FitnessClass.objects.get(id=class_id)
        except FitnessClass.DoesNotExist:
            logger.error(f"Fitness class with id {class_id} not found")
            return Response({'error': 'Class not found.'}, status=status.HTTP_404_NOT_FOUND)

        if fitness_class.available_slots <= 0:
            logger.warning(f"No slots available for class id {class_id}")
            return Response({'error': 'No slots available.'}, status=status.HTTP_400_BAD_REQUEST)

        Booking.objects.create(
            fitness_class=fitness_class,
            client_name=client_name,
            client_email=client_email
        )

        fitness_class.available_slots -= 1
        fitness_class.save()

        logger.info(f"Booking successful for {client_email} in class id {class_id}")
        return Response({'message': 'Booking successful.'}, status=status.HTTP_201_CREATED)


class BookingListAPIView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        logger.info(f"Booking list requested for email: {email}")

        if not email:
            logger.warning("Booking list request missing email parameter")
            return Response({'error': 'Email parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EmailQuerySerializer(data={"email": email})
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        bookings = Booking.objects.filter(client_email=email)
        logger.info(f"Found {bookings.count()} bookings for email: {email}")

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
