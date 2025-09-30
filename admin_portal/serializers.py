# from rest_framework import serializers
# from .models import Doctor, Patient, Appointment

# # 🩺 Serializer for the Doctor model
# class DoctorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Doctor
#         fields = [
#             '_id', 'id_string', 'first_name', 'last_name', 'email', 'phone',
#             'gender', 'specialty', 'experience_years', 'status', 'created_at'
#         ]
#         read_only_fields = ['_id', 'created_at'] # These fields are set by the database/server

# # 👤 Serializer for the Patient model
# class PatientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Patient
#         fields = [
#             '_id', 'id_string', 'first_name', 'last_name', 'email', 'phone',
#             'gender', 'date_of_birth', 'blood_group', 'last_visit', 'created_at'
#         ]
#         read_only_fields = ['_id', 'created_at']

# # 🗓️ Serializer for the Appointment model
# class AppointmentSerializer(serializers.ModelSerializer):
#     # To display doctor/patient names instead of just their IDs
#     patient_name = serializers.CharField(source='patient.__str__', read_only=True)
#     doctor_name = serializers.CharField(source='doctor.__str__', read_only=True)

#     class Meta:
#         model = Appointment
#         fields = [
#             '_id', 'patient', 'doctor', 'patient_name', 'doctor_name',
#             'appointment_datetime', 'type', 'status', 'created_at'
#         ]
#         read_only_fields = ['_id', 'created_at', 'patient_name', 'doctor_name']


from rest_framework import serializers
from .models import (
    Doctor, Patient, Appointment, Address, EmergencyContact, 
    InsuranceInfo, ScheduleSettings
)

# --- Serializers for Embedded Documents ---
# These now inherit from serializers.Serializer and have no Meta class.
class AddressSerializer(serializers.Serializer):
    street = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    zip_code = serializers.CharField(max_length=20)

class EmergencyContactSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    relationship = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20)

class InsuranceInfoSerializer(serializers.Serializer):
    provider = serializers.CharField(max_length=255)
    policy_number = serializers.CharField(max_length=255)

class ScheduleSettingsSerializer(serializers.Serializer):
    working_days = serializers.JSONField(default=list)
    start_time = serializers.CharField(max_length=10)
    end_time = serializers.CharField(max_length=10)
    slot_duration = serializers.IntegerField(default=30)

# --- Main Model Serializers ---
class PatientSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    emergency_contact = EmergencyContactSerializer()
    insurance = InsuranceInfoSerializer(required=False, allow_null=True)

    class Meta:
        model = Patient
        fields = '__all__'

    def create(self, validated_data):
        # Pop nested data
        address_data = validated_data.pop('address')
        contact_data = validated_data.pop('emergency_contact')
        insurance_data = validated_data.pop('insurance', None)

        # ✅ Pass dicts directly, not model instances
        patient = Patient.objects.create(
            address=address_data,
            emergency_contact=contact_data,
            insurance=insurance_data,
            **validated_data
        )
        return patient


class DoctorSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    emergency_contact = EmergencyContactSerializer()
    schedule = ScheduleSettingsSerializer()

    class Meta:
        model = Doctor
        fields = '__all__'

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        contact_data = validated_data.pop('emergency_contact')
        schedule_data = validated_data.pop('schedule')

        # ✅ Pass dicts directly
        doctor = Doctor.objects.create(
            address=address_data,
            emergency_contact=contact_data,
            schedule=schedule_data,
            **validated_data
        )
        return doctor


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.__str__', read_only=True)
    doctor_name = serializers.CharField(source='doctor.__str__', read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'