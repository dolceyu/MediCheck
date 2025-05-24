from django.shortcuts import render, redirect
from app.models import Doctor
import logging
logger = logging.getLogger('app_logger')


def index(request):
    context = {'is_logged_in': request.user.is_authenticated}
    return render(request, 'index.html', context)

def choose_registration(request):
    return render(request, 'choose_registration.html')

def register_patient(request):
    return render(request, 'register_patient.html')

from django.contrib import messages
from django.contrib.auth.models import User
from .models import Doctor

from .models import ValidLicense  

def register_doctor(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        license_number = request.POST.get('license_number')

        if not ValidLicense.objects.filter(license_number=license_number).exists():
            messages.error(request, "Номер ліцензії недійсний або не знайдено в базі.")
            return render(request, 'register_doctor.html')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Користувач з таким email вже існує.")
            return render(request, 'register_doctor.html')

        if Doctor.objects.filter(license_number=license_number).exists():
            messages.error(request, "Лікар з таким номером ліцензії вже існує.")
            return render(request, 'register_doctor.html')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        print("User створено:", user.username)

        Doctor.objects.create(
            last_name=request.POST.get('last_name'),
            first_name=request.POST.get('first_name'),
            middle_name=request.POST.get('middle_name'),
            gender=request.POST.get('gender'),
            dob=request.POST.get('dob'),
            email=email,
            license_number=license_number,
            password=password
        )
        logger.info(f'Успішна реєстрація лікаря: {email}')
        return render(request, 'registration_success.html')

    return render(request, 'register_doctor.html')



from .models import Patient

from django.contrib.auth.models import User

def register_patient(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user, created = User.objects.get_or_create(username=email, defaults={
            'email': email
        })
        if created:
            user.set_password(password)
            user.save()
            print("User створено:", user.username)
        else:
            print("User вже існує")

        if not Patient.objects.filter(email=email).exists():
            Patient.objects.create(
                last_name=request.POST.get('last_name'),
                first_name=request.POST.get('first_name'),
                middle_name=request.POST.get('middle_name'),
                gender=request.POST.get('gender'),
                dob=request.POST.get('dob'),
                email=email,
                password=password 
            )
            print("Пацієнта збережено")
        else:
            print("Пацієнт вже існує")

        logger.info(f'Успішна реєстрація пацієнта: {email}')
        return render(request, 'registration_success.html')  

    return render(request, 'register_patient.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

from app.models import Patient, Doctor

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print("Логін за email:", email)
        logger.info(f'Спроба входу: {email}')

        try:
            user = User.objects.get(username=email)
            print("User знайдений:", user.username)

            auth_user = authenticate(username=user.username, password=password)
            if auth_user is not None:
                print("Пароль правильний, логінимо користувача")
                logger.info(f'Успішний вхід: {email}')
                login(request, auth_user)

                if Patient.objects.filter(email=email).exists():
                    print("Це пацієнт!")
                    logger.info(f'Пацієнт {email} увійшов у систему')
                    return redirect('patient_dashboard')
                elif Doctor.objects.filter(email=email).exists():
                    print("Це лікар!")
                    logger.info(f'Лікар {email} увійшов у систему')
                    return redirect('doctor_dashboard')
                else:
                    print("Не знайдено ні пацієнта, ні лікаря!")
                    logger.warning(f'Невідома роль користувача: {email}')
                    return redirect('index')

            else:
                print("Невірний пароль або User не активний")
                logger.warning(f'Невдала спроба входу (невірний пароль): {email}')
                messages.error(request,'Невірний email або пароль.')

        except User.DoesNotExist:
            print("Користувача з таким email не знайдено")
            logger.warning(f'Спроба входу з неіснуючим email: {email}')
            messages.error(request, 'Користувача з таким email не знайдено.')

    return render(request, 'login.html')




def patient_dashboard(request):
    patient = Patient.objects.get(email=request.user.email)
    return render(request, 'patient_dashboard.html', {'patient': patient})

from .models import Doctor

def doctor_dashboard(request):
    doctor = None
    if request.user.is_authenticated:
        try:
            doctor = Doctor.objects.get(email=request.user.email)
        except Doctor.DoesNotExist:
            pass
    return render(request, 'doctor_dashboard.html', {'doctor': doctor})



from django.shortcuts import render, get_object_or_404, redirect
from .models import MedicalService, SurveyQuestion, SurveyAnswer, SurveyComment, Patient
from django.contrib.auth.decorators import login_required

@login_required
def survey_view(request, service_slug):
    service = get_object_or_404(MedicalService, slug=service_slug)
    patient = get_object_or_404(Patient, email=request.user.email)
    questions = SurveyQuestion.objects.filter(for_role='patient')

    if request.method == 'POST':
        for question in questions:
            rating = request.POST.get(f'q{question.id}')
            if rating:
                SurveyAnswer.objects.create(
                    user=request.user,
                    service=service,
                    question=question,
                    rating=int(rating)
                )
        comment = request.POST.get('comment')
        if comment:
            SurveyComment.objects.create(
                user=request.user,
                service=service,
                text=comment
            )
        logger.info(f'Пацієнт {request.user.email} надіслав анкету для сервісу: {service.name}')
        return redirect('survey_thank_you')

    return render(request, 'survey_patient.html', {
        'patient': patient,
        'service': service,
        'questions': questions
    })

def survey_thank_you(request):
    return render(request, 'survey_thank_you.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import MedicalService, SurveyQuestion, SurveyAnswer, SurveyComment, Doctor

from collections import defaultdict

@login_required
def survey_doctor_view(request, service_slug):
    service = get_object_or_404(MedicalService, slug=service_slug)
    doctor = get_object_or_404(Doctor, email=request.user.email)
    questions = SurveyQuestion.objects.filter(for_role='doctor')

    questions_by_category = defaultdict(list)
    for q in questions:
        questions_by_category[q.category].append(q)

    if request.method == 'POST':
        for question in questions:
            rating = request.POST.get(f'q{question.id}')
            if rating:
                SurveyAnswer.objects.create(
                    user=request.user,
                    service=service,
                    question=question,
                    rating=int(rating)
                )
        comment = request.POST.get('comment')
        if comment:
            SurveyComment.objects.create(
                user=request.user,
                service=service,
                text=comment
            )
        logger.info(f'Лікар {request.user.email} надіслав анкету для сервісу: {service.name}')
        return redirect('survey_thank_you')

    return render(request, 'survey_doctor.html', {
        'doctor': doctor,
        'service': service,
        'questions_by_category': dict(questions_by_category)
    })



from django.shortcuts import render
from .models import MedicalService, SurveyQuestion, SurveyAnswer
from django.db.models import Q 
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import MedicalService, SurveyQuestion, SurveyAnswer, SurveyComment
import logging

logger = logging.getLogger(__name__)

@staff_member_required
def admin_stats(request):
    services = MedicalService.objects.all()
    roles = ['patient', 'doctor']
    questions = SurveyQuestion.objects.all()
    chart_data = None
    comments = []

    selected_service = None
    selected_role = None
    selected_question_id = None
    selected_chart = None

    if request.method == 'POST':
        selected_service = request.POST.get('service')
        selected_role = request.POST.get('role')
        selected_question_id = request.POST.get('question')  
        selected_chart = request.POST.get('chart_type')

        service = MedicalService.objects.filter(name=selected_service).first()
        question = SurveyQuestion.objects.filter(id=selected_question_id, for_role=selected_role).first()

        if service and question:
            answers = SurveyAnswer.objects.filter(service=service, question=question)
            chart_data = {i: answers.filter(rating=i).count() for i in range(1, 6)}

            comments = SurveyComment.objects.filter(
                service=service,
                user__isnull=False
            ).order_by('-submitted_at')

        logger.info(f'Адміністратор {request.user.email} переглянув статистику для сервісу: {selected_service}, питання ID: {selected_question_id}')

    return render(request, 'admin_stats.html', {
        'services': services,
        'roles': roles,
        'questions': questions,
        'chart_data': chart_data,
        'comments': comments,
        'selected_service': selected_service,
        'selected_role': selected_role,
        'selected_question': int(selected_question_id) if selected_question_id else None,
        'selected_chart': selected_chart or 'bar',
    })

from django.http import JsonResponse

def get_questions_by_role(request):
    role = request.GET.get('role')
    questions = SurveyQuestion.objects.filter(for_role=role)
    data = [{'id': q.id, 'text': q.text} for q in questions]
    return JsonResponse({'questions': data})

@login_required
def profile_patient(request):
    patient = get_object_or_404(Patient, email=request.user.email)
    return render(request, 'profile_patient.html', {'patient': patient})

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password


@login_required
def profile_doctor(request):
    doctor = get_object_or_404(Doctor, email=request.user.email)
    return render(request, 'profile_doctor.html', {'doctor': doctor})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from app.models import Patient, Doctor

from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib import messages
import logging

logger = logging.getLogger('app_logger')

@login_required
def change_password_view(request):
    user = request.user
    role = None
    profile = None

    if Patient.objects.filter(email=user.email).exists():
        role = 'patient'
        profile = Patient.objects.get(email=user.email)
    elif Doctor.objects.filter(email=user.email).exists():
        role = 'doctor'
        profile = Doctor.objects.get(email=user.email)

    if not profile:
        return render(request, 'change_password.html', {'error': 'Користувач не знайдений.'})

    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']

        if not user.check_password(old_password):
            return render(request, 'change_password.html', {
                'error': 'Старий пароль невірний.',
                'role': role
            })

        user.set_password(new_password)
        user.save()

        logout(request)
        messages.success(request, 'Пароль успішно змінено. Увійдіть знову.')
        logger.info(f'Користувач {user.email} змінив пароль і вийшов із системи')

        return redirect('login')  

    return render(request, 'change_password.html', {'role': role})

from django.contrib.auth.decorators import login_required
from app.models import SurveyAnswer, SurveyQuestion, MedicalService

@login_required
def doctor_ratings(request):
    user = request.user
    selected_service = request.GET.get('service')

    services = MedicalService.objects.filter(
        surveyanswer__user=user
    ).distinct()

    ratings = SurveyAnswer.objects.filter(user=user).select_related('question', 'service')

    if selected_service:
        ratings = ratings.filter(service__id=selected_service)

    return render(request, 'doctor_ratings.html', {
        'ratings': ratings,
        'services': services,
        'selected_service': int(selected_service) if selected_service else None
    })

@login_required
def patient_ratings(request):
    user = request.user
    selected_service = request.GET.get('service')

    all_services = SurveyAnswer.objects.filter(user=user).values_list('service__name', flat=True).distinct()
    ratings = SurveyAnswer.objects.filter(user=user).select_related('question', 'service')

    if selected_service:
        ratings = ratings.filter(service__name=selected_service)

    return render(request, 'patient_ratings.html', {
        'ratings': ratings,
        'services': all_services,
        'selected_service': selected_service,
    })

from django.shortcuts import render

def about(request):
    return render(request, 'about.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def support_view(request):
    return render(request, 'support.html')

from django.http import HttpResponse
import csv, json
from app.models import SurveyAnswer

@staff_member_required
def export_answers_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="survey_answers.csv"'

    writer = csv.writer(response)
    writer.writerow(['Користувач', 'Сервіс', 'Питання', 'Оцінка'])

    for ans in SurveyAnswer.objects.select_related('user', 'service', 'question'):
        writer.writerow([ans.user.email, ans.service.name, ans.question.text, ans.rating])

    return response

@staff_member_required
def export_answers_json(request):
    answers = SurveyAnswer.objects.select_related('user', 'service', 'question')
    data = [
        {
            'user': a.user.email,
            'service': a.service.name,
            'question': a.question.text,
            'rating': a.rating
        } for a in answers
    ]
    return HttpResponse(
        json.dumps(data, ensure_ascii=False, indent=2),
        content_type='application/json'
    )
