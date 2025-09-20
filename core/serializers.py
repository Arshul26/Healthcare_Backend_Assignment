from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Patient, Doctor, PatientDoctorMapping

# ----------------------------
# User Registration Serializer
# ----------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

# ----------------------------
# Patient Serializer
# ----------------------------
class PatientSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Patient
        fields = '__all__'

# ----------------------------
# Doctor Serializer
# ----------------------------
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'contact_number', 'email', 'created_at']
        read_only_fields = ['created_at']

# ----------------------------
# Patient-Doctor Mapping Serializer
# ----------------------------
class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), write_only=True, source='patient'
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), write_only=True, source='doctor'
    )

    class Meta:
        model = PatientDoctorMapping
        fields = ('id', 'patient', 'doctor', 'patient_id', 'doctor_id', 'assigned_at')
        read_only_fields = ('assigned_at',)
