from datetime import datetime, timedelta, time
from .models import Appointment

# Mapping: Vaccine ID to weekday
VACCINE_DAY_MAP = {
    1: 0,  # Monday
    2: 1,  # Tuesday
    3: 2,  # Wednesday
    4: 3,  # Thursday
    5: 4,  # Friday
}

TIME_SLOTS = [time(8, 0), time(8, 15), time(8, 30), time(8, 45)]


def get_next_available_slot(vaccine_id):
    target_weekday = VACCINE_DAY_MAP[vaccine_id]
    today = datetime.today().date()

    # Find next target_weekday
    for i in range(1, 30):  # look ahead 30 days
        candidate_date = today + timedelta(days=i)
        if candidate_date.weekday() == target_weekday:
            appointments = Appointment.objects.filter(vaccination_date=candidate_date)
            booked_times = set(a.time for a in appointments)
            for slot in TIME_SLOTS:
                if slot not in booked_times:
                    return candidate_date, slot
    return None, None  # fully booked
