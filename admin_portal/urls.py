# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import DoctorViewSet, PatientViewSet, AppointmentViewSet,DashboardStatsView

# # Create a router and register our viewsets with it.
# router = DefaultRouter()
# router.register(r'doctors', DoctorViewSet, basename='doctor')
# router.register(r'patients', PatientViewSet, basename='patient')
# router.register(r'appointments', AppointmentViewSet, basename='appointment')

# # The API URLs are now determined automatically by the router.
# urlpatterns = [
#     path('', include(router.urls)),
#     path('dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
#]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.dashboard_views import DashboardStatsView
from .views.doctor_views import DoctorViewSet
from .views.patient_views import PatientViewSet
from .views.appointment_views import AppointmentViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('', include(router.urls)),
]