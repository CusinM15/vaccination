# 💉 Vaccination App

Vaccination App is a simple appointment booking system for vaccinations. Users can register, confirm their email and book a vaccination from one of five available types:

- COVID-19
- Influenza (Flu)
- Hepatitis A
- Tetanus
- MMR (Measles, Mumps, Rubella)

### ✅ Steps Taken

1. Project started as a **local Django project using SQLite**.
2. It was then **Dockerized**, still using SQLite inside the container.
3. Later, a **migration to PostgreSQL** was performed.


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


#### Reminder
🚀 How to Run the Reminder Command

- In Docker (with HOST: 'db' in settings.py):
Make sure your containers are running:

```bash
docker-compose up -d
```

Run the reminder command inside the web container:

```bash
docker-compose exec web python manage.py send_reminders
```

- Locally (with HOST: 'localhost' in settings.py):
Activate your virtual environment:

```bash
.\venv\Scripts\activate
```

Run the reminder command:

```bash
python manage.py send_reminders
```

🕒 How to Schedule the Reminder Automatically
1. On Linux/macOS (using cron):
Edit your crontab:
Add a line to run the command every day at 8:00 AM:
1. On Windows (using Task Scheduler):
Open Task Scheduler.
Create a new task:
Action: Start a program
Program/script:
Add arguments:
Start in:
Set the trigger (e.g., daily at 8:00 AM).

⚠️ Note
The reminder will NOT run automatically unless you set up a scheduled job (cron, Task Scheduler, etc.).
You must run the command manually or automate it as described above.

## ⚙️ Tech Stack

- 🐍 Python (Django Framework)
- 🗃️ SQLite or PostgreSQL
- 📬 Email system via Django
- 🐳 Docker support 

```python
'HOST': 'localhost'     # for local DB
'HOST': 'db'            # for Docker PostgreSQL container
```

## 🐳 Running with Docker


You can run this app easily using Docker without installing Python or dependencies on your machine.

```bash
git clone https://github.com/CusinM15/vaccination.git
cd vaccination
docker build -t vaccination-app .
docker run -p 8000:8000 vaccination-app
```

Or, using Docker Compose (recommended for development):

```bash
git clone https://github.com/CusinM15/vaccination.git
cd vaccination
docker-compose up --build
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🛠️ Getting Started (without Docker)

```bash
git clone https://github.com/CusinM15/vaccination.git
cd vaccination
python -m venv venv
source venv\Scripts\activate 
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
