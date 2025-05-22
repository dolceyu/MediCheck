from django.db import models

class Doctor(models.Model):
    GENDER_CHOICES = [('male', 'Чоловік'), ('female', 'Жінка')]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    license_number = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # тимчасово, пізніше зробимо хешування

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Patient(models.Model):
    GENDER_CHOICES = [
        ('male', 'Чоловік'),
        ('female', 'Жінка'),
    ]

    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    

from django.db import models
from django.contrib.auth.models import User

class MedicalService(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class SurveyQuestion(models.Model):
    ROLE_CHOICES = [
        ('patient', 'Пацієнт'),
        ('doctor', 'Лікар'),
    ]

    CATEGORY_CHOICES = [
        ('interface', 'Доступність та зручність інтерфейсу'),
        ('mobile', 'Мобільна адаптація'),
        ('speed', 'Швидкодія та стабільність'),
        ('booking', 'Запис на прийом'),
        ('trust', 'Довіра та безпека'),
        ('general', 'Загальне враження'),
    ]
    
    text = models.TextField()
    for_role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='general'  # 👈 важливо, інакше база зламаєтьс 
        )

    def __str__(self):
        return self.text

class SurveyAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(MedicalService, on_delete=models.CASCADE)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1-5
    submitted_at = models.DateTimeField(auto_now_add=True)

class SurveyComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(MedicalService, on_delete=models.CASCADE)
    text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

class ValidLicense(models.Model):
    license_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.license_number
