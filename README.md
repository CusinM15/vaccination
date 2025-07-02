# 💉 Vaccination App

Vaccination App is a simple appointment booking system for vaccinations. Users can register, confirm their email, and book a vaccination from one of five available types:

- COVID-19
- Influenza (Flu)
- Hepatitis A
- Tetanus
- MMR (Measles, Mumps, Rubella)

## 🧩 Key Features

- ✅ **Email confirmation required** before booking an appointment.
- 📅 **One vaccination per day**, each vaccine is administered on a specific weekday:
  - Monday: COVID-19  
  - Tuesday: Influenza  
  - Wednesday: Hepatitis A  
  - Thursday: Tetanus  
  - Friday: MMR
- ⏱️ **Appointments are scheduled between 08:00 and 09:00** (working days only).
- 👥 **15-minute time slots** allow up to 4 patients per day.
- ✉️ **Email notifications**:
  - Confirmation email upon registration
  - Reminder email **1 week before** your appointment

## ⚙️ Tech Stack

- 🐍 Python (Django Framework)
- 🗃️ SQLite for development (planned migration to PostgreSQL)
- 📬 Email system via Django
- 🐳 Docker support (in progress, planned)

## 🚀 Future Plans

- [ ] Create and publish a Docker image for easy deployment
- [ ] Migrate from SQLite to PostgreSQL
- [ ] Improve frontend styling and responsiveness
- [ ] Add admin dashboard for managing bookings

## 🐳 Running with Docker

You can run this app easily using Docker without installing Python or dependencies on your machine.

```bash
git clone https://github.com/your-username/vaccination-app.git
cd vaccination-app
docker build -t vaccination-app .
docker run -p 8000:8000 vaccination-app
```

Or, using Docker Compose (recommended for development):

```bash
git clone https://github.com/your-username/vaccination-app.git
cd vaccination-app
docker-compose up --build
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🛠️ Getting Started (without Docker)

```bash
git clone https://github.com/your-username/vaccination-app.git
cd vaccination-app
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
