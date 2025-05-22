from django.contrib import admin
from app.models import Doctor

admin.site.register(Doctor)

from .models import Patient

admin.site.register(Patient)

from django.contrib import admin
from .models import MedicalService, SurveyQuestion, SurveyAnswer, SurveyComment

admin.site.register(MedicalService)
admin.site.register(SurveyQuestion)
admin.site.register(SurveyAnswer)
admin.site.register(SurveyComment)

from django.contrib import admin
from .models import ValidLicense

admin.site.register(ValidLicense)
