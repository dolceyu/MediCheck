from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('choose/', views.choose_registration, name='choose_registration'),
    path('register/patient/', views.register_patient, name='register_patient'),
    path('register/doctor/', views.register_doctor, name='register_doctor'),
    path('login/', views.login_view, name='login'),  
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('survey/thank-you/', views.survey_thank_you, name='survey_thank_you'),
    path('survey/<slug:service_slug>/', views.survey_view, name='survey'),
    path('survey/<slug:service_slug>/doctor/', views.survey_doctor_view, name='survey_doctor'),
    path('admin-stats/', views.admin_stats, name='admin_stats'),
    path('get-questions/', views.get_questions_by_role, name='get_questions_by_role'),
    path('profile/patient/', views.profile_patient, name='profile_patient'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('doctor/profile/', views.profile_doctor, name='profile_doctor'),
    path('doctor/change-password/', views.change_password_view, name='change_password'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('doctor/ratings/', views.doctor_ratings, name='doctor_ratings'),
    path('patient/ratings/', views.patient_ratings, name='patient_ratings'),
    path('about/', views.about, name='about'),
    path('support/', views.support_view, name='support'),
    path('export/answers/csv/', views.export_answers_csv, name='export_answers_csv'),
    path('export/answers/json/', views.export_answers_json, name='export_answers_json'),
]

