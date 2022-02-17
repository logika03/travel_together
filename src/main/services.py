from datetime import datetime

from django.db.models import Prefetch, Q

from main.models import Trip


def get_trips(pk, is_available: bool):
    return Trip.objects.filter(
        Q(author=pk) | Q(participants__participant__id=pk),
        is_available=is_available).order_by('date')


def get_available_trips():
    return Trip.objects.filter(is_available=True).order_by('date')


def change_trip_status():
    for trip in Trip.objects.filter(is_available=True):
        if trip.date < datetime.now().date():
            trip.is_available = False
            trip.save()
