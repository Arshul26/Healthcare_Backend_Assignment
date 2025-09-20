from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    PatientListCreateView,
    PatientRetrieveUpdateDestroyView,
    DoctorListCreateView,
    DoctorRetrieveUpdateDestroyView,
    PatientDoctorMappingListCreateView,
    PatientDoctorMappingRetrieveView,
    PatientDoctorMappingDestroyView,
)

urlpatterns = [
    # Authentication
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),

    # Patients
    path('patients/', PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:id>/', PatientRetrieveUpdateDestroyView.as_view(), name='patient-detail'),

    # Doctors
    path('doctors/', DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('doctors/<int:id>/', DoctorRetrieveUpdateDestroyView.as_view(), name='doctor-detail'),

    # Patient-Doctor Mappings
    path('mappings/', PatientDoctorMappingListCreateView.as_view(), name='mapping-list-create'),
    path('mappings/<int:patient_id>/', PatientDoctorMappingRetrieveView.as_view(), name='mapping-by-patient'),
    path('mappings/<int:id>/delete/', PatientDoctorMappingDestroyView.as_view(), name='mapping-delete'),
]
