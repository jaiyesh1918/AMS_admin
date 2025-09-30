# from rest_framework import viewsets, permissions
# from ..models import Patient
# from ..serializers import PatientSerializer
# from ..permissions import IsAdminUser
# # from django.shortcuts import get_object_or_404

# class PatientViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows admins to view, create, edit, or delete patients.
#     """
#     queryset = Patient.objects.all().order_by('last_name')
#     serializer_class = PatientSerializer
#     lookup_field = '_id'
#     permission_classes = [permissions.IsAuthenticated, IsAdminUser]
   

from rest_framework import viewsets, permissions
from bson import ObjectId
from django.http import Http404
from ..models import Patient
from ..serializers import PatientSerializer
from ..permissions import IsAdminUser

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('last_name')
    serializer_class = PatientSerializer
    lookup_field = '_id'
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        _id = self.kwargs.get(lookup_url_kwarg)

        try:
            obj = Patient.objects.get(_id=ObjectId(_id))
        except Patient.DoesNotExist:
            raise Http404

        self.check_object_permissions(self.request, obj)
        return obj
