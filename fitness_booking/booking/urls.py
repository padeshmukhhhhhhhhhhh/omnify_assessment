from django.urls import path
from .views import ClassListAPIView, BookClassAPIView, BookingListAPIView

urlpatterns = [
    path('classes/', ClassListAPIView.as_view()),
    path('book/', BookClassAPIView.as_view()),
    path('bookings/', BookingListAPIView.as_view()),
]
