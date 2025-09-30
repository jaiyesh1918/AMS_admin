# from rest_framework import viewsets, permissions
# from ..models import Appointment
# from ..serializers import AppointmentSerializer
# from ..permissions import IsAdminUser

# class AppointmentViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows admins to view, create, edit, or delete appointments.
#     """
#     queryset = Appointment.objects.all().order_by('-appointment_datetime')
#     serializer_class = AppointmentSerializer
#     permission_classes = [permissions.IsAuthenticated, IsAdminUser]
from rest_framework import viewsets, permissions
from bson import ObjectId
from django.http import Http404
from ..models import Appointment
from ..serializers import AppointmentSerializer
from ..permissions import IsAdminUser

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().order_by('-appointment_datetime')
    serializer_class = AppointmentSerializer
    lookup_field = '_id'
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        _id = self.kwargs.get(lookup_url_kwarg)

        try:
            obj = Appointment.objects.get(_id=ObjectId(_id))
        except Appointment.DoesNotExist:
            raise Http404

        self.check_object_permissions(self.request, obj)
        return obj
