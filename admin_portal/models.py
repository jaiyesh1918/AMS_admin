# from djongo import models

# # 🩺 Based on the "Doctor Management" UI
# class Doctor(models.Model):
#     GENDER_CHOICES = [
#         ('male', 'Male'),
#         ('female', 'Female'),
#         ('other', 'Other'),
#     ]
#     STATUS_CHOICES = [
#         ('active', 'Active'),
#         ('inactive', 'Inactive'),
#     ]

#     _id = models.ObjectIdField()
#     id_string = models.CharField(max_length=100, unique=True, verbose_name="Display ID") # For DOC001
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=20)
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
#     specialty = models.CharField(max_length=100)
#     experience_years = models.PositiveIntegerField(default=0)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'doctors'  # Explicitly name the MongoDB collection

#     def __str__(self):
#         return f"Dr. {self.first_name} {self.last_name}"


# # 👤 Based on the "Patient Management" UI
# class Patient(models.Model):
#     GENDER_CHOICES = [
#         ('male', 'Male'),
#         ('female', 'Female'),
#         ('other', 'Other'),
#     ]

#     _id = models.ObjectIdField()
#     id_string = models.CharField(max_length=100, unique=True, verbose_name="Display ID") # For Patient ID
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=20)
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
#     date_of_birth = models.DateField()
#     blood_group = models.CharField(max_length=5, blank=True)
#     last_visit = models.DateField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'patients' # Explicitly name the MongoDB collection

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"


# # 🗓️ Based on the "Appointment Overview" UI
# class Appointment(models.Model):
#     STATUS_CHOICES = [
#         ('scheduled', 'Scheduled'),
#         ('completed', 'Completed'),
#         ('cancelled', 'Cancelled'),
#         ('no-show', 'No-Show'),
#     ]
#     TYPE_CHOICES = [
#         ('consultation', 'Consultation'),
#         ('follow-up', 'Follow-up'),
#         ('procedure', 'Procedure'),
#         ('check-up', 'Check-up'),
#     ]

#     _id = models.ObjectIdField()
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
#     appointment_datetime = models.DateTimeField()
#     type = models.CharField(max_length=20, choices=TYPE_CHOICES)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'appointments' # Explicitly name the MongoDB collection
#         ordering = ['-appointment_datetime']

#     def __str__(self):
#         return f"Appointment for {self.patient} with {self.doctor} on {self.appointment_datetime.strftime('%Y-%m-%d %H:%M')}"



from djongo import models
from django.db import models as django_models


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20, verbose_name="ZIP Code")
    class Meta: abstract = True

class EmergencyContact(models.Model):
    full_name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    class Meta: abstract = True

class InsuranceInfo(models.Model):
    provider = models.CharField(max_length=255)
    policy_number = models.CharField(max_length=255)
    class Meta: abstract = True

class ScheduleSettings(models.Model):
    working_days = django_models.JSONField(default=list)
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    slot_duration = models.IntegerField(default=30)
    class Meta: abstract = True

# --- Main Models ---

class Patient(models.Model):
    
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    _id = models.ObjectIdField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES) # Applied choices
    blood_type = models.CharField(max_length=5, blank=True)
    address = models.EmbeddedField(model_container=Address) 
    emergency_contact = models.EmbeddedField(model_container=EmergencyContact)
    insurance = models.EmbeddedField(model_container=InsuranceInfo, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active') # Applied choices
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'patients'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Doctor(models.Model):
    # 👇 Added CHOICES
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]

    _id = models.ObjectIdField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True) # Applied choices
    specialization = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    qualifications = django_models.JSONField(default=list)
    licenseNumber = models.CharField(max_length=100, null=True, blank=True)
    address = models.EmbeddedField(model_container=Address ,null=True)
    emergency_contact = models.EmbeddedField(model_container=EmergencyContact ,null=True)
    schedule = models.EmbeddedField(model_container=ScheduleSettings ,null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active') # Applied choices
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'doctors'

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

class Appointment(models.Model):
    STATUS_CHOICES = [('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('no-show', 'No-Show')]
    TYPE_CHOICES = [('consultation', 'Consultation'), ('follow-up', 'Follow-up'), ('procedure', 'Procedure'), ('check-up', 'Check-up')]

    _id = models.ObjectIdField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_datetime = models.DateTimeField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appointments'
        ordering = ['-appointment_datetime']

    def __str__(self):
        return f"Appointment for {self.patient} with {self.doctor} on {self.appointment_datetime.strftime('%Y-%m-%d %H:%M')}"