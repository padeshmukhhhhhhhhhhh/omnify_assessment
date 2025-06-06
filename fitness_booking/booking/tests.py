from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import FitnessClass
from django.utils.timezone import now, timedelta

class FitnessClassAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.cls = FitnessClass.objects.create(
            name='Pilates',
            instructor='Emma',
            start_time=now() + timedelta(days=1),
            total_slots=10,
            available_slots=10
        )

    def test_class_list_api(self):
        response = self.client.get('/api/classes/?tz=Asia/Kolkata')  # Adjust path to your route
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('name' in response.data[0])

    def test_booking_api(self):
        response = self.client.post('/api/book/', {
            'class_id': self.cls.id,
            'client_name': 'Bob',
            'client_email': 'bob@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_booking_list_api(self):
        # Create a booking first
        self.client.post('/api/book/', {
            'class_id': self.cls.id,
            'client_name': 'Charlie',
            'client_email': 'charlie@example.com'
        })
        response = self.client.get('/api/bookings/?email=charlie@example.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_booking_list_api_missing_email(self):
        response = self.client.get('/api/bookings/')  # No email param
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Email parameter is required.')

