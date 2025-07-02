from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from pendulum import now, parse, date
from appointment.utils import get_next_available_slot
from .models import Appointment, User, Vaccine
from .forms import RegisterForm
from django.core.mail import send_mail
from django.conf import settings
import secrets
from datetime import date
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Appointment, Vaccine
from .utils import get_next_available_slot  # adjust if needed


def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        return render(request, 'appointment/login.html', {'message': "Invalid credentials"})
    return render(request, 'appointment/login.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            token = user.confirmation_token
            user.save()
            confirm_link = request.build_absolute_uri(f"/confirm/{token}/")
            send_mail(
                subject="Confirm your email",
                message=f"Click to confirm: {confirm_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            return render(request, 'appointment/register.html', {'form': form, 'message': "Check your email to confirm."})
        return render(request, 'appointment/register.html', {'form': form, 'message': "Invalid input."})
    else:
        form = RegisterForm()
    return render(request, 'appointment/register.html', {'form': form})

def confirm_email(request, token):
    try:
        user = User.objects.get(confirmation_token=token)
        user.is_confirmed = True
        user.confirmation_token = None
        user.save()
        return render(request, 'appointment/confirm_email.html', {'message': "Email confirmed!"})
    except User.DoesNotExist:
        return render(request, 'appointment/confirm_email.html', {'message': "Invalid token!"})

@login_required
def resend_verification(request):
    if request.method == "POST":
        user = request.user
        last_sent = request.session.get('last_verification_sent')
        if last_sent:
            try:
                elapsed = now() - parse(last_sent)
                if elapsed.total_seconds() < 120:
                    return redirect('dashboard')
            except ValueError:
                pass
        token = secrets.token_hex(32)
        user.confirmation_token = token
        user.save()
        confirm_link = request.build_absolute_uri(f"/confirm/{token}/")
        send_mail(
            subject="Resend: Confirm your email",
            message=f"Click to confirm: {confirm_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        request.session['last_verification_sent'] = now().isoformat()
        return redirect('dashboard')

@login_required
def submit_vacation(request):
    if request.method == "POST":
        user = request.user
        vaccination = request.POST['vaccination']
        vaccination_dates = {
            'COVID-19': date(2025, 8, 15),
            'Flu': date(2025, 12, 20),
            'Hepatitis A': date(2025, 9, 5),
            'Tetanus': date(2025, 10, 10),
            'MMR': date(2025, 7, 25)
        }
        Appointment.objects.create(
            user=user,
            vaccination=vaccination,
            signup_date=now(),
            vaccination_date=vaccination_dates.get(vaccination, date.today())
        )
        return redirect('dashboard')
    return render(request, 'appointment/submit_vaccination.html')

@login_required
def dashboard(request):
    user = request.user
    signups = Appointment.objects.filter(user=user)
    vaccines = Vaccine.objects.all()
    can_resend = False
    time_remaining = 0
    last_sent = request.session.get('last_verification_sent')
    if not user.is_confirmed:
        if last_sent:
            try:
                last_sent_dt = parse(last_sent)
                elapsed = now() - last_sent_dt
                if elapsed.total_seconds() > 120:
                    can_resend = True
                else:
                    time_remaining = 120 - int(elapsed.total_seconds())
            except ValueError:
                can_resend = True
        else:
            can_resend = True

    return render(request, 'appointment/dashboard.html', {
        'user': user,
        'vaccines': vaccines,
        'signups': signups,
        'can_resend': can_resend,
        'time_remaining': time_remaining
    })

@login_required
def book_appointment(request):
    if request.method == 'POST':
        user = request.user
        vaccine_id = int(request.POST['vaccine_id'])
        date, time_slot = get_next_available_slot(vaccine_id)

        if not date or not time_slot:
            return render(request, 'no_slots.html')

        # ✅ Check if this user already booked on this day
        if Appointment.objects.filter(user=user, vaccination_date=date).exists():
            messages.error(request, "You already have an appointment on this day.")
            return redirect("dashboard")

        # ✅ Create appointment
        appointment = Appointment.objects.create(
            user=user,
            vaccine_id=vaccine_id,
            vaccination_date=date,
            time=time_slot
        )

        # ✅ Send confirmation email
        send_mail(
            'Vaccination Appointment Confirmed',
            f'You are scheduled for vaccination on {date} at {time_slot}.',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )

        messages.success(request, "Appointment booked successfully!")
        return redirect('dashboard')
    return redirect('dashboard')

    