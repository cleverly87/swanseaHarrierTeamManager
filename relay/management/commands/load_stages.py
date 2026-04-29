"""
Load the actual Welsh Castles Relay 2026 stages into the database.
Run with: python manage.py load_stages
"""
from django.core.management.base import BaseCommand
from relay.models import Stage


STAGES = [
    {
        'stage_number': 1, 'name': 'Caernarfon to Penygroes', 'day': 1, 'distance_miles': 9.1, 'is_mountain': False,
        'start_time': '10:00', 'start_location_name': 'Caernarfon Castle',
        'start_location_address': 'Main Entrance Stairs in Castle Ditch, LL55 2AU',
        'end_location_name': 'Penygroes', 'end_location_address': 'Penygroes side of footbridge, near Wynnstay Stores, LL54 6NR',
        'description': 'Start and registration at Caernarfon Castle main entrance stairs. Finish is at the Penygroes side of the footbridge near Wynnstay Stores.',
        'mens_record': '50:45', 'mens_record_year': 2024, 'womens_record': '56:53', 'womens_record_year': 2025,
    },
    {
        'stage_number': 2, 'name': 'Penygroes to Criccieth', 'day': 1, 'distance_miles': 10.7, 'is_mountain': False,
        'start_time': '11:00', 'start_location_name': 'Penygroes',
        'start_location_address': 'Cycle track (Lôn Eifion) near A487 roundabout, Penygroes, LL54 6LY',
        'end_location_name': 'Criccieth', 'end_location_address': 'The Green, Criccieth, LL52 0HB',
        'description': 'Start is on the cycle track near the A487 roundabout in Penygroes. Finish is on the green in Criccieth.',
        'mens_record': '53:33', 'mens_record_year': 2025, 'womens_record': '62:46', 'womens_record_year': 2022,
    },
    {
        'stage_number': 3, 'name': 'Criccieth to Maentwrog', 'day': 1, 'distance_miles': 12.3, 'is_mountain': True,
        'start_time': '11:55', 'start_location_name': 'Criccieth',
        'start_location_address': 'The Green / A497, Criccieth, LL52 0HB',
        'end_location_name': 'Maentwrog', 'end_location_address': 'Oakeley Arms Hotel, Maentwrog, LL41 3YU',
        'description': 'Start is on the green in Criccieth. Finish is at the Oakeley Arms Hotel in Maentwrog.',
        'mens_record': '59:36', 'mens_record_year': 2025, 'womens_record': '73:02', 'womens_record_year': 2005,
    },
    {
        'stage_number': 4, 'name': 'Maentwrog to Harlech', 'day': 1, 'distance_miles': 9.5, 'is_mountain': False,
        'start_time': '13:00', 'start_location_name': 'Maentwrog',
        'start_location_address': 'Oakeley Arms Hotel, Maentwrog, LL41 3YU',
        'end_location_name': 'Harlech', 'end_location_address': 'Ysgol Ardudwy School car park, Harlech, LL46 2UB',
        'description': 'Start is near the Oakeley Arms in Maentwrog. Finish is at Ysgol Ardudwy School in Harlech.',
        'mens_record': '47:43', 'mens_record_year': 2024, 'womens_record': '54:37', 'womens_record_year': 2011,
    },
    {
        'stage_number': 5, 'name': 'Harlech to Barmouth', 'day': 1, 'distance_miles': 9.6, 'is_mountain': False,
        'start_time': '13:50', 'start_location_name': 'Harlech',
        'start_location_address': 'A496 near level crossing, Harlech, LL46 2UB',
        'end_location_name': 'Barmouth', 'end_location_address': 'Barmouth town centre / seafront area, LL42 1NE',
        'description': 'Start is on the A496 near the level crossing in Harlech. Finish is in Barmouth town centre near the seafront.',
        'mens_record': '50:08', 'mens_record_year': 2013, 'womens_record': '60:05', 'womens_record_year': 2024,
    },
    {
        'stage_number': 6, 'name': 'Barmouth to Dolgellau', 'day': 1, 'distance_miles': 9.0, 'is_mountain': False,
        'start_time': '14:40', 'start_location_name': 'Barmouth',
        'start_location_address': 'Barmouth, LL42 1NE',
        'end_location_name': 'Dolgellau', 'end_location_address': 'Dolgellau, LL40 1AR',
        'description': 'Start is in Barmouth. Finish is in Dolgellau town centre area.',
        'mens_record': '49:32', 'mens_record_year': 2019, 'womens_record': '61:48', 'womens_record_year': 2019,
    },
    {
        'stage_number': 7, 'name': 'Dolgellau to Dinas Mawddwy', 'day': 1, 'distance_miles': 10.1, 'is_mountain': True,
        'start_time': '15:35', 'start_location_name': 'Dolgellau',
        'start_location_address': 'Dolgellau, LL40 1AR',
        'end_location_name': 'Dinas Mawddwy', 'end_location_address': 'Dinas Mawddwy, SY20 9LP',
        'description': 'Start is in Dolgellau. Finish is in Dinas Mawddwy village.',
        'mens_record': '54:39', 'mens_record_year': 2024, 'womens_record': '65:43', 'womens_record_year': 2024,
    },
    {
        'stage_number': 8, 'name': 'Dinas Mawddwy to Foel', 'day': 1, 'distance_miles': 10.8, 'is_mountain': False,
        'start_time': '16:25', 'start_location_name': 'Dinas Mawddwy',
        'start_location_address': 'Dinas Mawddwy, SY20 9LP',
        'end_location_name': 'Foel', 'end_location_address': 'Foel (rural changeover point), SY21 0NU',
        'description': 'Start is in Dinas Mawddwy. Finish is at a rural changeover point near Foel.',
        'mens_record': '56:27', 'mens_record_year': 2025, 'womens_record': '67:45', 'womens_record_year': 2023,
    },
    {
        'stage_number': 9, 'name': 'Foel to Llanfair Caereinion', 'day': 1, 'distance_miles': 8.5, 'is_mountain': False,
        'start_time': '17:10', 'start_location_name': 'Foel',
        'start_location_address': 'Foel, SY21 0NU',
        'end_location_name': 'Llanfair Caereinion', 'end_location_address': 'Llanfair Caereinion, SY21 0QZ',
        'description': 'Start is at the Foel changeover point. Finish is in Llanfair Caereinion.',
        'mens_record': '43:32', 'mens_record_year': 2004, 'womens_record': '47:02', 'womens_record_year': 2015,
    },
    {
        'stage_number': 10, 'name': 'Llanfair Caereinion to Newtown', 'day': 1, 'distance_miles': 13.1, 'is_mountain': True,
        'start_time': '17:50', 'start_location_name': 'Llanfair Caereinion',
        'start_location_address': 'Llanfair Caereinion, SY21 0QZ',
        'end_location_name': 'Newtown', 'end_location_address': 'Newtown (town centre / leisure centre area), SY16 2NZ',
        'description': 'Start is in Llanfair Caereinion. Finish is in Newtown near the town centre and leisure facilities.',
        'mens_record': '65:12', 'mens_record_year': 2024, 'womens_record': '77:55', 'womens_record_year': 2022,
    },
    {
        'stage_number': 11, 'name': 'Newtown to Llanbadarn Fynydd', 'day': 2, 'distance_miles': 10.5, 'is_mountain': True,
        'start_time': '07:00', 'start_location_name': 'Newtown',
        'start_location_address': 'Newtown, SY16 2NZ',
        'end_location_name': 'Llanbadarn Fynydd', 'end_location_address': 'Llanbadarn Fynydd, LD1 6YA',
        'description': 'Start is in Newtown. Finish is in Llanbadarn Fynydd.',
        'mens_record': '55:27', 'mens_record_year': 2025, 'womens_record': '67:27', 'womens_record_year': 2024,
    },
    {
        'stage_number': 12, 'name': 'Llanbadarn Fynydd to Crossgates', 'day': 2, 'distance_miles': 11.2, 'is_mountain': False,
        'start_time': '07:55', 'start_location_name': 'Llanbadarn Fynydd',
        'start_location_address': 'Llanbadarn Fynydd, LD1 6YA',
        'end_location_name': 'Crossgates', 'end_location_address': 'Crossgates, LD1 6RF',
        'description': 'Start is in Llanbadarn Fynydd. Finish is at Crossgates.',
        'mens_record': '53:33', 'mens_record_year': 1993, 'womens_record': '63:29', 'womens_record_year': 2025,
    },
    {
        'stage_number': 13, 'name': 'Crossgates to Builth Wells', 'day': 2, 'distance_miles': 10.6, 'is_mountain': False,
        'start_time': '08:50', 'start_location_name': 'Crossgates',
        'start_location_address': 'Crossgates, LD1 6RF',
        'end_location_name': 'Builth Wells', 'end_location_address': 'Builth Wells, LD2 3DL',
        'description': 'Start is at Crossgates. Finish is in Builth Wells.',
        'mens_record': '52:19', 'mens_record_year': 1998, 'womens_record': '62:51', 'womens_record_year': 2009,
    },
    {
        'stage_number': 14, 'name': 'Builth Wells to Drovers Arms', 'day': 2, 'distance_miles': 10.8, 'is_mountain': True,
        'start_time': '09:45', 'start_location_name': 'Builth Wells',
        'start_location_address': 'Builth Wells, LD2 3DL',
        'end_location_name': 'Drovers Arms', 'end_location_address': 'Drovers Arms (A40), LD3 0SG',
        'description': 'Start is in Builth Wells. Finish is at the Drovers Arms on the A40.',
        'mens_record': '57:28', 'mens_record_year': 2024, 'womens_record': '66:41', 'womens_record_year': 2024,
    },
    {
        'stage_number': 15, 'name': 'Epynt Visitor Centre to Brecon', 'day': 2, 'distance_miles': 12.8, 'is_mountain': False,
        'start_time': '10:45', 'start_location_name': 'Epynt Visitor Centre',
        'start_location_address': 'Epynt Visitor Centre, LD3 8NL',
        'end_location_name': 'Brecon', 'end_location_address': 'Brecon, LD3 7EW',
        'description': 'Start is at Epynt Visitor Centre. Finish is in Brecon town centre area.',
        'mens_record': '64:03', 'mens_record_year': 2025, 'womens_record': '75:44', 'womens_record_year': 2015,
    },
    {
        'stage_number': 16, 'name': 'Brecon Canal Basin to Torpantau', 'day': 2, 'distance_miles': 12.5, 'is_mountain': True,
        'start_time': '11:45', 'start_location_name': 'Brecon Canal Basin',
        'start_location_address': 'Brecon Canal Basin, LD3 7EW',
        'end_location_name': 'Torpantau', 'end_location_address': 'Torpantau, LD3 8NL',
        'description': 'Start is at Brecon Canal Basin. Finish is at Torpantau in the Brecon Beacons.',
        'mens_record': '66:58', 'mens_record_year': 2024, 'womens_record': '83:29', 'womens_record_year': 2025,
    },
    {
        'stage_number': 17, 'name': 'Taf Fechan Railway Station, Torpantau to Cyfarthfa Castle', 'day': 2, 'distance_miles': 8.7, 'is_mountain': False,
        'start_time': '12:30', 'start_location_name': 'Taf Fechan Railway Station, Torpantau',
        'start_location_address': 'Taf Fechan Railway Station, Torpantau, LD3 8NL',
        'end_location_name': 'Cyfarthfa Castle', 'end_location_address': 'Cyfarthfa Castle, Merthyr Tydfil, CF47 8RE',
        'description': 'Start is at Taf Fechan railway station near Torpantau. Finish is at Cyfarthfa Castle in Merthyr.',
        'mens_record': '44:45', 'mens_record_year': 2019, 'womens_record': '53:12', 'womens_record_year': 2018,
    },
    {
        'stage_number': 18, 'name': 'Rhydycar LC to Navigation Park', 'day': 2, 'distance_miles': 9.1, 'is_mountain': False,
        'start_time': '13:30', 'start_location_name': 'Rhydycar Leisure Centre',
        'start_location_address': 'Rhydycar Leisure Centre, Merthyr Tydfil, CF48 1UT',
        'end_location_name': 'Navigation Park', 'end_location_address': 'Navigation Park, Abercynon, CF45 4SN',
        'description': 'Start is at Rhydycar Leisure Centre. Finish is at Navigation Park in Abercynon.',
        'mens_record': '45:53', 'mens_record_year': 2024, 'womens_record': '49:52', 'womens_record_year': 2011,
    },
    {
        'stage_number': 19, 'name': 'Navigation Park to Nantgarw', 'day': 2, 'distance_miles': 7.7, 'is_mountain': False,
        'start_time': '14:15', 'start_location_name': 'Navigation Park',
        'start_location_address': 'Navigation Park, Abercynon, CF45 4SN',
        'end_location_name': 'Nantgarw', 'end_location_address': 'Nantgarw, CF15 7QX',
        'description': 'Start is at Navigation Park. Finish is in Nantgarw.',
        'mens_record': '38:49', 'mens_record_year': 2025, 'womens_record': '47:48', 'womens_record_year': 2025,
    },
    {
        'stage_number': 20, 'name': 'Caerphilly to Cardiff', 'day': 2, 'distance_miles': 9.1, 'is_mountain': False,
        'start_time': '14:50', 'start_location_name': 'Caerphilly Castle',
        'start_location_address': 'Caerphilly Castle, CF83 1JD',
        'end_location_name': 'Cardiff', 'end_location_address': 'Pontcanna Fields (Cardiff finish area), CF11 9LB',
        'description': 'Start is at Caerphilly Castle. Finish is at Pontcanna Fields in Cardiff for the race finish and presentations.',
        'mens_record': '50:14', 'mens_record_year': 2023, 'womens_record': '55:39', 'womens_record_year': 2022,
    },
]


class Command(BaseCommand):
    help = 'Load the Welsh Castles Relay 2026 stages (20 stages with actual route data)'

    def handle(self, *args, **options):
        self.stdout.write("Loading Welsh Castles Relay 2026 stages...")

        # Clear existing stages
        Stage.objects.all().delete()
        self.stdout.write("Cleared existing stages.")

        # Create stages
        for stage_data in STAGES:
            stage = Stage.objects.create(**stage_data)
            stage_type = "⛰ Mountain" if stage.is_mountain else "🛣 Road"
            self.stdout.write(
                f"  Stage {stage.stage_number}: {stage.name} - {stage.distance_miles} miles ({stage.distance_km:.2f} km) {stage_type}"
            )

        self.stdout.write(self.style.SUCCESS(f"\n✓ Successfully loaded {len(STAGES)} stages!"))
        self.stdout.write(self.style.SUCCESS("  Day 1 (June 6th): Stages 1-10"))
        self.stdout.write(self.style.SUCCESS("  Day 2 (June 7th): Stages 11-20"))
