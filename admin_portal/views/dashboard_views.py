from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.utils import timezone
import datetime
from ..models import Doctor, Patient, Appointment
from ..serializers import AppointmentSerializer
from ..permissions import IsAdminUser

class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        start_of_day = datetime.datetime.combine(today, datetime.time.min)
        end_of_day = datetime.datetime.combine(today, datetime.time.max)
        
        todays_appointments = Appointment.objects.filter(appointment_datetime__range=(start_of_day, end_of_day))
        
        data = {
            'total_doctors': Doctor.objects.count(),
            'total_patients': Patient.objects.count(),
            'todays_appointments_count': todays_appointments.count(),
            'todays_schedule': AppointmentSerializer(todays_appointments, many=True).data
        }
        return Response(data)