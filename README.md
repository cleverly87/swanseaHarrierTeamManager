# Welsh Castles Relay – Swansea Harriers Team Manager

A Django web application for managing the **Welsh Castles Relay** – a 20-stage relay race from North Wales to South Wales over two days.

## Features

### Public-facing pages
| Page | URL | Description |
|------|-----|-------------|
| Relay Overview | `/` | All 20 stages across Day 1 & Day 2 with athlete assignments, stage type, start times and locations |
| Stage Detail | `/stage/<n>/` | Full details: distance, type (mountain/road), start time, athlete report time, full address |
| Team Roster | `/team/` | All athletes in the 40-person squad with their assigned stage(s) |
| Accommodation | `/accommodation/` | Hotels, rooms and who is staying where |
| Checklist | `/checklist/` | Team manager task checklist with priorities, due dates and status |

### Admin (backend) – `/admin/`
- **Athletes** – manage the squad of up to 40 runners
- **Stages** – configure all 20 stages (name, distance, mountain/road, times, locations, assign runner)
- **Support Staff** – drivers, medics, coordinators etc.
- **Hotels** – add hotels with check-in/check-out dates and room breakdown
- **Hotel Rooms** – define rooms per hotel with type and capacity
- **Hotel Bookings** – assign athletes or support staff to specific rooms
- **Checklist Tasks** – manage the pre-race task list with priorities and deadlines

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Apply database migrations
```bash
python manage.py migrate
```

### 3. (Optional) Load sample data
This seeds all 20 stages with Welsh Castles Relay routes, 40 athletes, sample hotels and 20 checklist tasks:
```bash
python manage.py seed_data
```

### 4. Create an admin account
```bash
python manage.py createsuperuser
```

### 5. Start the development server
```bash
python manage.py runserver
```

Visit:
- **Public site** → http://127.0.0.1:8000/
- **Admin panel** → http://127.0.0.1:8000/admin/

## Production Deployment

### Live Site
The application is hosted on **PythonAnywhere**:
- **Production URL** → https://cleverly87.eu.pythonanywhere.com/
- **Admin panel** → https://cleverly87.eu.pythonanywhere.com/admin/

### Deploying Changes

When you make changes locally and want to update the live site:

#### 1. Commit and push your changes
```cmd
git add .
git commit -m "Description of your changes"
git push origin main
```

#### 2. Update the production server
Log into PythonAnywhere, open a Bash console, and run:
```bash
cd ~/swanseaHarrierTeamManager
source venv/bin/activate
git pull origin main
```

#### 3. Run migrations (if you changed models)
```bash
python manage.py migrate
```

#### 4. Collect static files (if you changed CSS/JS/images)
```bash
python manage.py collectstatic --noinput
```

#### 5. Reload the web app
Go to the **Web** tab on PythonAnywhere and click the green **Reload** button.

### Important Notes
- Always test changes locally before deploying to production
- Database changes on the live site must be done through the admin panel or by exporting/importing data
- Never commit sensitive data like passwords or secret keys to the repository

## Project Layout
```
castles_relay/          Django project settings & URL conf
relay/
  models.py             Athlete, Stage, SupportStaff, Hotel, HotelRoom, HotelBooking, ChecklistTask
  views.py              Public-facing views
  admin.py              Admin configuration for all models
  urls.py               URL routing for the relay app
  management/commands/
    seed_data.py        Management command to load sample data
  tests.py              Unit & integration tests
templates/
  base.html             Base template with navigation
  relay/
    home.html           Relay overview (all stages)
    stage_detail.html   Individual stage page
    team_roster.html    Team athlete list
    accommodation.html  Hotel & room assignments
    checklist.html      Team manager task checklist
static/css/main.css     Welsh-themed stylesheet
```

## Running Tests
```bash
python manage.py test relay
```
