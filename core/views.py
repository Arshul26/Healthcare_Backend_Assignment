from rest_framework import generics, status, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    RegisterSerializer,
    PatientSerializer,
    DoctorSerializer,
    PatientDoctorMappingSerializer
)

# ----------------------------
# User Registration
# ----------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# ----------------------------
# User Login
# ----------------------------
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# ----------------------------
# Patient CRUD
# ----------------------------
class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PatientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)


# ----------------------------
# Doctor CRUD
# ----------------------------
class DoctorListCreateView(generics.ListCreateAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    queryset = Doctor.objects.all()


class DoctorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    queryset = Doctor.objects.all()


# ----------------------------
# Patient-Doctor Mapping
# ----------------------------
class PatientDoctorMappingListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    queryset = PatientDoctorMapping.objects.all()


class PatientDoctorMappingRetrieveView(generics.ListAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return PatientDoctorMapping.objects.filter(patient_id=patient_id)


class PatientDoctorMappingDestroyView(generics.DestroyAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    queryset = PatientDoctorMapping.objects.all()



# from django.db import IntegrityError
# from django.db.models import Q
# from django.shortcuts import get_object_or_404

# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.views import APIView

# from django.contrib.auth import get_user_model

# from .models import Patient, Doctor, PatientDoctorMapping
# from .serializers import RegisterSerializer, PatientSerializer, DoctorSerializer, PatientDoctorMappingSerializer
# from .permissions import IsOwner

# User = get_user_model()

# # Register
# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = RegisterSerializer

#     def create(self, request, *args, **kwargs):
#         return super().create(request, *args, **kwargs)

# # Patients
# class PatientListCreateView(generics.ListCreateAPIView):
#     serializer_class = PatientSerializer
#     permission_classes = (IsAuthenticated,)

#     def get_queryset(self):
#         return Patient.objects.filter(created_by=self.request.user).order_by("-created_at")

#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user)

# class PatientRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = PatientSerializer
#     permission_classes = (IsAuthenticated, IsOwner)
#     lookup_field = "pk"

#     def get_queryset(self):
#         # Ownership enforced by permission, but restrict queryset for safety
#         return Patient.objects.filter(created_by=self.request.user)

# # Doctors
# class DoctorListCreateView(generics.ListCreateAPIView):
#     serializer_class = DoctorSerializer

#     def get_permissions(self):
#         # Allow anyone to list/get doctors, but require auth for create/update/delete
#         if self.request.method == "GET":
#             return [AllowAny()]
#         return [IsAuthenticated()]

#     def get_queryset(self):
#         return Doctor.objects.all().order_by("-created_at")

# class DoctorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = DoctorSerializer

#     def get_permissions(self):
#         # anyone can retrieve, but updates/deletes need auth
#         if self.request.method in ("GET",):
#             return [AllowAny()]
#         return [IsAuthenticated()]

#     def get_queryset(self):
#         return Doctor.objects.all()

# # Mappings
# class PatientDoctorMappingListCreateView(generics.ListCreateAPIView):
#     serializer_class = PatientDoctorMappingSerializer
#     permission_classes = (IsAuthenticated,)

#     def get_queryset(self):
#         # Return mappings related to the requesting user (their patients or assigned by them)
#         return PatientDoctorMapping.objects.filter(
#             Q(patient__created_by=self.request.user) | Q(assigned_by=self.request.user)
#         ).select_related("patient", "doctor", "assigned_by")

#     def create(self, request, *args, **kwargs):
#         patient_id = request.data.get("patient")
#         doctor_id = request.data.get("doctor")
#         if not patient_id or not doctor_id:
#             return Response({"detail": "patient and doctor are required"}, status=status.HTTP_400_BAD_REQUEST)

#         patient = get_object_or_404(Patient, pk=patient_id)
#         if patient.created_by != request.user:
#             return Response({"detail": "You can only assign doctors to your own patients."}, status=status.HTTP_403_FORBIDDEN)

#         doctor = get_object_or_404(Doctor, pk=doctor_id)

#         try:
#             mapping = PatientDoctorMapping.objects.create(patient=patient, doctor=doctor, assigned_by=request.user)
#         except IntegrityError:
#             return Response({"detail": "This doctor is already assigned to this patient."}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = self.get_serializer(mapping)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class PatientDoctorsListView(generics.ListAPIView):
#     serializer_class = PatientDoctorMappingSerializer
#     permission_classes = (IsAuthenticated,)

#     def get(self, request, patient_id, *args, **kwargs):
#         patient = get_object_or_404(Patient, pk=patient_id)
#         if patient.created_by != request.user:
#             return Response({"detail": "You can only view mappings for your own patients."}, status=status.HTTP_403_FORBIDDEN)
#         mappings = PatientDoctorMapping.objects.filter(patient=patient).select_related("doctor", "assigned_by")
#         serializer = self.get_serializer(mappings, many=True)
#         return Response(serializer.data)

# class PatientDoctorMappingDeleteView(generics.DestroyAPIView):
#     serializer_class = PatientDoctorMappingSerializer
#     permission_classes = (IsAuthenticated,)

#     def get_queryset(self):
#         # allow delete only if the mapping is related to your patient or you assigned it
#         return PatientDoctorMapping.objects.filter(
#             Q(patient__created_by=self.request.user) | Q(assigned_by=self.request.user)
#         )

#     def delete(self, request, *args, **kwargs):
#         return super().delete(request, *args, **kwargs)
