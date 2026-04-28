"""
Seed the database with sample Welsh Castles Relay data.
Run with: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from relay.models import Athlete, Stage, SupportStaff, Hotel, HotelRoom, ChecklistTask


ATHLETES = [
    ("Rhys", "Williams"), ("Sian", "Jones"), ("Gareth", "Evans"), ("Nia", "Davies"),
    ("Owain", "Roberts"), ("Bethan", "Thomas"), ("Huw", "Hughes"), ("Cerys", "Morgan"),
    ("Dylan", "Lewis"), ("Ffion", "Price"), ("Ieuan", "Jenkins"), ("Lowri", "Edwards"),
    ("Cai", "Phillips"), ("Angharad", "Griffiths"), ("Macsen", "Davies"), ("Megan", "Powell"),
    ("Tomos", "Harris"), ("Nerys", "James"), ("Emlyn", "White"), ("Carys", "Green"),
    ("Bryn", "Brown"), ("Seren", "Clark"), ("Alun", "Thompson"), ("Lona", "Turner"),
    ("Gruffudd", "Robinson"), ("Elen", "Hall"), ("Rhodri", "Young"), ("Gwen", "Walker"),
    ("Peredur", "King"), ("Branwen", "Wright"), ("Caradog", "Hill"), ("Morfudd", "Scott"),
    ("Taliesin", "Wilson"), ("Blodwen", "Baker"), ("Cadoc", "Carter"), ("Einir", "Mitchell"),
    ("Aneirin", "Anderson"), ("Tegwen", "Martin"), ("Cadfan", "Taylor"), ("Aeron", "Moore"),
]

STAGES = [
    # (num, name, day, dist, mountain, start, report, start_name, start_addr, end_name, end_addr)
    (1,  "Conwy to Llanrwst",          1,  9.8, False, "07:00", "06:30",
     "Conwy Castle", "Rose Hill Street, Conwy LL32 8AY", "Llanrwst Market Square", "Station Road, Llanrwst LL26 0DG"),
    (2,  "Llanrwst to Betws-y-Coed",   1,  7.3, False, "07:55", "07:25",
     "Llanrwst Market Square", "Station Road, Llanrwst LL26 0DG", "Betws-y-Coed Village", "Holyhead Road, Betws-y-Coed LL24 0AH"),
    (3,  "Betws-y-Coed to Swallow Falls",1,11.5, True,  "09:00", "08:25",
     "Betws-y-Coed Village", "Holyhead Road, Betws-y-Coed LL24 0AH", "Swallow Falls Car Park", "A5, Betws-y-Coed LL24 0DH"),
    (4,  "Swallow Falls to Capel Curig", 1,  6.2, True,  "10:20", "09:50",
     "Swallow Falls Car Park", "A5, Betws-y-Coed LL24 0DH", "Capel Curig Village", "A5, Capel Curig LL24 0EL"),
    (5,  "Capel Curig to Pen-y-Gwryd",  1, 10.1, True,  "11:15", "10:45",
     "Capel Curig Village", "A5, Capel Curig LL24 0EL", "Pen-y-Gwryd Hotel", "Nant Gwynant, Llanberis LL55 4NT"),
    (6,  "Pen-y-Gwryd to Beddgelert",   1,  8.4, True,  "12:30", "12:00",
     "Pen-y-Gwryd Hotel", "Nant Gwynant, Llanberis LL55 4NT", "Beddgelert Village", "Waterloo Bridge, Beddgelert LL55 4UY"),
    (7,  "Beddgelert to Porthmadog",    1, 12.7, False, "13:45", "13:15",
     "Beddgelert Village", "Waterloo Bridge, Beddgelert LL55 4UY", "Porthmadog Harbour", "Harbour Road, Porthmadog LL49 9AD"),
    (8,  "Porthmadog to Harlech",       1, 14.2, False, "15:10", "14:40",
     "Porthmadog Harbour", "Harbour Road, Porthmadog LL49 9AD", "Harlech Castle", "Castle Square, Harlech LL46 2YH"),
    (9,  "Harlech to Barmouth",         1, 10.9, False, "16:45", "16:15",
     "Harlech Castle", "Castle Square, Harlech LL46 2YH", "Barmouth Bridge", "The Promenade, Barmouth LL42 1HB"),
    (10, "Barmouth to Dolgellau",       1,  9.3, False, "18:00", "17:30",
     "Barmouth Bridge", "The Promenade, Barmouth LL42 1HB", "Dolgellau Town Square", "Eldon Square, Dolgellau LL40 1PY"),
    (11, "Dolgellau to Machynlleth",    2,  18.6, False, "07:30", "07:00",
     "Dolgellau Town Square", "Eldon Square, Dolgellau LL40 1PY", "Machynlleth Clock Tower", "Maengwyn Street, Machynlleth SY20 8EB"),
    (12, "Machynlleth to Aberystwyth",  2,  20.4, False, "09:00", "08:30",
     "Machynlleth Clock Tower", "Maengwyn Street, Machynlleth SY20 8EB", "Aberystwyth Promenade", "Marine Terrace, Aberystwyth SY23 2AZ"),
    (13, "Aberystwyth to Aberaeron",    2,  16.1, False, "11:30", "11:00",
     "Aberystwyth Promenade", "Marine Terrace, Aberystwyth SY23 2AZ", "Aberaeron Harbour", "Quay Street, Aberaeron SA46 0BT"),
    (14, "Aberaeron to Lampeter",       2,  13.8, False, "13:00", "12:30",
     "Aberaeron Harbour", "Quay Street, Aberaeron SA46 0BT", "Lampeter Town Centre", "High Street, Lampeter SA48 7BG"),
    (15, "Lampeter to Llandovery",      2,  17.2, True,  "14:30", "14:00",
     "Lampeter Town Centre", "High Street, Lampeter SA48 7BG", "Llandovery Castle", "Castle Road, Llandovery SA20 0AB"),
    (16, "Llandovery to Brecon",        2,  19.4, True,  "16:15", "15:45",
     "Llandovery Castle", "Castle Road, Llandovery SA20 0AB", "Brecon Cathedral", "Cathedral Close, Brecon LD3 9DP"),
    (17, "Brecon to Merthyr Tydfil",    2,  16.8, True,  "18:00", "17:30",
     "Brecon Cathedral", "Cathedral Close, Brecon LD3 9DP", "Merthyr Tydfil Civic Centre", "Castle Street, Merthyr Tydfil CF47 8AN"),
    (18, "Merthyr Tydfil to Pontypridd",2,  12.4, False, "19:30", "19:00",
     "Merthyr Tydfil Civic Centre", "Castle Street, Merthyr Tydfil CF47 8AN", "Pontypridd Town Bridge", "Bridge Street, Pontypridd CF37 4PE"),
    (19, "Pontypridd to Cardiff North", 2,  11.6, False, "20:30", "20:00",
     "Pontypridd Town Bridge", "Bridge Street, Pontypridd CF37 4PE", "Llandaff Cathedral", "Cathedral Close, Llandaff, Cardiff CF5 2YF"),
    (20, "Cardiff North to Cardiff Castle", 2,  7.8, False, "21:30", "21:00",
     "Llandaff Cathedral", "Cathedral Close, Llandaff, Cardiff CF5 2YF", "Cardiff Castle", "Castle Street, Cardiff CF10 3NB"),
]

HOTELS = [
    {
        "name": "Snowdonia Lodge",
        "address": "High Street, Betws-y-Coed LL24 0AN",
        "phone": "01690 710123",
        "check_in": "2025-06-13",
        "check_out": "2025-06-14",
        "notes": "Night 1 accommodation for all athletes and support staff doing Day 1 stages.",
        "rooms": [
            ("101", "twin", 2),
            ("102", "twin", 2),
            ("103", "twin", 2),
            ("104", "twin", 2),
            ("105", "double", 2),
            ("106", "double", 2),
            ("107", "triple", 3),
            ("108", "triple", 3),
        ],
    },
    {
        "name": "Cardigan Bay Hotel",
        "address": "Marine Terrace, Aberystwyth SY23 2BX",
        "phone": "01970 612345",
        "check_in": "2025-06-14",
        "check_out": "2025-06-15",
        "notes": "Midpoint hotel between Day 1 finish and Day 2 start.",
        "rooms": [
            ("201", "twin", 2),
            ("202", "twin", 2),
            ("203", "twin", 2),
            ("204", "double", 2),
            ("205", "family", 4),
        ],
    },
]

TASKS = [
    ("Confirm all 20 athletes for stages", "high", "2025-05-01", "Team Manager"),
    ("Book hotel night 1 – Snowdonia Lodge", "high", "2025-04-15", "Team Manager"),
    ("Book hotel night 2 – Cardigan Bay", "high", "2025-04-15", "Team Manager"),
    ("Send athlete information pack", "high", "2025-05-15", "Team Manager"),
    ("Arrange team transport/minibus for Day 1", "high", "2025-04-30", "Team Manager"),
    ("Arrange team transport/minibus for Day 2", "high", "2025-04-30", "Team Manager"),
    ("Confirm first aid provision", "high", "2025-05-20", "Coordinator"),
    ("Order team kit and vests", "medium", "2025-05-01", "Team Manager"),
    ("Prepare race number bibs", "medium", "2025-06-01", "Coordinator"),
    ("Set up water/feed stations", "medium", "2025-06-10", "Support Staff"),
    ("Circulate route maps to all athletes", "medium", "2025-05-20", "Team Manager"),
    ("Confirm emergency contact forms received", "high", "2025-06-01", "Team Manager"),
    ("Brief all drivers on stage handover points", "medium", "2025-06-12", "Coordinator"),
    ("Pack first aid kit for Day 1 convoy", "high", "2025-06-13", "Medic"),
    ("Pack first aid kit for Day 2 convoy", "high", "2025-06-13", "Medic"),
    ("Check weather forecast and brief team", "low", "2025-06-12", "Team Manager"),
    ("Hotel check-in list prepared", "medium", "2025-06-10", "Team Manager"),
    ("Collect athlete entry fees", "medium", "2025-04-30", "Team Manager"),
    ("Submit official entry to Welsh Castles Relay", "high", "2025-04-01", "Team Manager"),
    ("Post-event team celebration booked", "low", "2025-06-01", "Team Manager"),
]


class Command(BaseCommand):
    help = 'Seed the database with sample Welsh Castles Relay data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding athletes…')
        athletes = []
        for fn, ln in ATHLETES:
            obj, _ = Athlete.objects.get_or_create(first_name=fn, last_name=ln)
            athletes.append(obj)

        self.stdout.write('Seeding stages…')
        for i, s in enumerate(STAGES):
            num, name, day, dist, mtn, start, report, sn, sa, en, ea = s
            stage, _ = Stage.objects.get_or_create(
                stage_number=num,
                defaults=dict(
                    name=name, day=day, distance_km=dist, is_mountain=mtn,
                    start_time=start, athlete_report_time=report,
                    start_location_name=sn, start_location_address=sa,
                    end_location_name=en, end_location_address=ea,
                    athlete=athletes[i] if i < len(athletes) else None,
                )
            )

        self.stdout.write('Seeding support staff…')
        SupportStaff.objects.get_or_create(
            first_name='John', last_name='Owen',
            defaults={'role': 'manager', 'phone': '07700 900001'}
        )
        SupportStaff.objects.get_or_create(
            first_name='Helen', last_name='Price',
            defaults={'role': 'medic', 'phone': '07700 900002'}
        )
        SupportStaff.objects.get_or_create(
            first_name='Paul', last_name='Davies',
            defaults={'role': 'driver', 'phone': '07700 900003'}
        )
        SupportStaff.objects.get_or_create(
            first_name='Sue', last_name='Williams',
            defaults={'role': 'coordinator', 'phone': '07700 900004'}
        )

        self.stdout.write('Seeding hotels…')
        from datetime import date
        for h in HOTELS:
            hotel, _ = Hotel.objects.get_or_create(
                name=h['name'],
                defaults=dict(
                    address=h['address'], phone=h['phone'],
                    check_in_date=h['check_in'], check_out_date=h['check_out'],
                    total_rooms_booked=len(h['rooms']), notes=h['notes']
                )
            )
            for rid, rtype, cap in h['rooms']:
                HotelRoom.objects.get_or_create(
                    hotel=hotel, room_identifier=rid,
                    defaults={'room_type': rtype, 'capacity': cap}
                )

        self.stdout.write('Seeding checklist tasks…')
        for title, priority, due, assigned in TASKS:
            ChecklistTask.objects.get_or_create(
                title=title,
                defaults={'priority': priority, 'due_date': due, 'assigned_to': assigned}
            )

        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
