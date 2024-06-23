from django.urls import path
from .views import home_view, seat_availability_view, college_view

urlpatterns = [
    path('', home_view, name='home'),
    path('live', seat_availability_view, name='seat_availability'),
    path('college/<str:college_name>/', college_view, name='college_view'),
]