# appointment/management/commands/send_reminders.py

from django.core.management.base import BaseCommand
from appointment.models import Appointment
from django.utils.timezone import now
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Send email reminders for appointments scheduled 7 days from today.'

    def handle(self, *args, **kwargs):
        reminder_date = now().date() + timedelta(days=7)
        appointments = Appointment.objects.filter(vaccination_date=reminder_date)

        if not appointments.exists():
            self.stdout.write(f"No appointments found for {reminder_date}.")
            return

        count = 0
        for a in appointments:
            try:
                send_mail(
                    subject='Vaccination Reminder',
                    message=f'Hello {a.user.first_name},\n\n'
                            f'This is a reminder that your vaccination ({a.vaccine.name}) '
                            f'is scheduled for {a.vaccination_date} at {a.time}.\n\n'
                            f'Please arrive on time.\n\nBest regards,\nVaccination Center',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[a.user.email],
                    fail_silently=False,
                )
                count += 1
                self.stdout.write(f"Reminder sent to {a.user.email}")
            except Exception as e:
                self.stderr.write(f"Failed to send to {a.user.email}: {e}")

        self.stdout.write(self.style.SUCCESS(f"Successfully sent {count} reminders for {reminder_date}."))
