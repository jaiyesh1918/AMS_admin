# from rest_framework import viewsets, permissions
# from ..models import Doctor
# from ..serializers import DoctorSerializer
# from ..permissions import IsAdminUser

# class DoctorViewSet(viewsets.ModelViewSet):
#     queryset = Doctor.objects.all().order_by('last_name')
#     serializer_class = DoctorSerializer
#     permission_classes = [permissions.IsAuthenticated, IsAdminUser]
from rest_framework import viewsets, permissions
from bson import ObjectId
from django.http import Http404
from ..models import Doctor
from ..serializers import DoctorSerializer
from ..permissions import IsAdminUser

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all().order_by('last_name')
    serializer_class = DoctorSerializer
    lookup_field = '_id'
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        _id = self.kwargs.get(lookup_url_kwarg)

        try:
            obj = Doctor.objects.get(_id=ObjectId(_id))
        except Doctor.DoesNotExist:
            raise Http404

        self.check_object_permissions(self.request, obj)
        return obj
