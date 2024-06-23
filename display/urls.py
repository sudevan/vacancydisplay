from django.urls import path
from . import views
from .views import seat_availability_view
urlpatterns = [
    path('', seat_availability_view, name='seat_availability'),
]