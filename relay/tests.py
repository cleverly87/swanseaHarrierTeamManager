from django.test import TestCase, Client
from django.urls import reverse
from .models import Athlete, Stage, SupportStaff, Hotel, HotelRoom, HotelBooking, ChecklistTask


class AthleteModelTest(TestCase):
    def setUp(self):
        self.athlete = Athlete.objects.create(
            first_name='Rhys', last_name='Williams',
            email='rhys@example.com', phone='07700123456'
        )

    def test_str(self):
        self.assertEqual(str(self.athlete), 'Rhys Williams')

    def test_full_name(self):
        self.assertEqual(self.athlete.full_name, 'Rhys Williams')


class StageModelTest(TestCase):
    def setUp(self):
        self.athlete = Athlete.objects.create(first_name='Sian', last_name='Jones')
        self.stage = Stage.objects.create(
            stage_number=1,
            name='Conwy to Llanrwst',
            day=1,
            distance_km=9.8,
            is_mountain=False,
            start_time='07:00',
            athlete_report_time='06:30',
            start_location_name='Conwy Castle',
            start_location_address='Rose Hill Street, Conwy LL32 8AY',
            athlete=self.athlete,
        )

    def test_str(self):
        self.assertEqual(str(self.stage), 'Stage 1: Conwy to Llanrwst')

    def test_stage_type_label_road(self):
        self.assertEqual(self.stage.stage_type_label, 'Road')

    def test_stage_type_label_mountain(self):
        mountain_stage = Stage.objects.create(
            stage_number=3, name='Mountain Run', day=1, distance_km=11.5, is_mountain=True
        )
        self.assertEqual(mountain_stage.stage_type_label, 'Mountain')

    def test_athlete_linked(self):
        self.assertEqual(self.stage.athlete.full_name, 'Sian Jones')


class SupportStaffModelTest(TestCase):
    def setUp(self):
        self.staff = SupportStaff.objects.create(
            first_name='John', last_name='Owen', role='manager'
        )

    def test_str(self):
        self.assertIn('John Owen', str(self.staff))
        self.assertIn('Team Manager', str(self.staff))


class HotelAndBookingModelTest(TestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(
            name='Snowdonia Lodge',
            address='High Street, Betws-y-Coed',
            check_in_date='2025-06-13',
            check_out_date='2025-06-14',
        )
        self.room = HotelRoom.objects.create(
            hotel=self.hotel,
            room_identifier='101',
            room_type='twin',
            capacity=2,
        )
        self.athlete = Athlete.objects.create(first_name='Gareth', last_name='Evans')

    def test_hotel_str(self):
        self.assertEqual(str(self.hotel), 'Snowdonia Lodge')

    def test_room_str(self):
        self.assertIn('101', str(self.room))
        self.assertIn('Twin', str(self.room))

    def test_booking_athlete(self):
        booking = HotelBooking.objects.create(room=self.room, athlete=self.athlete)
        self.assertIn('Gareth Evans', str(booking))

    def test_booking_requires_person(self):
        from django.core.exceptions import ValidationError
        booking = HotelBooking(room=self.room)
        with self.assertRaises(ValidationError):
            booking.clean()

    def test_booking_cannot_have_both(self):
        from django.core.exceptions import ValidationError
        staff = SupportStaff.objects.create(first_name='Sue', last_name='Smith', role='driver')
        booking = HotelBooking(room=self.room, athlete=self.athlete, support_staff=staff)
        with self.assertRaises(ValidationError):
            booking.clean()


class ChecklistTaskModelTest(TestCase):
    def test_str_incomplete(self):
        task = ChecklistTask.objects.create(title='Book hotels', priority='high')
        self.assertIn('○', str(task))
        self.assertIn('Book hotels', str(task))

    def test_str_complete(self):
        task = ChecklistTask.objects.create(title='Book hotels', priority='high', completed=True)
        self.assertIn('✓', str(task))


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.athlete = Athlete.objects.create(first_name='Dylan', last_name='Lewis')
        self.stage = Stage.objects.create(
            stage_number=1,
            name='Conwy to Llanrwst',
            day=1,
            distance_km=9.8,
            is_mountain=False,
            athlete=self.athlete,
        )
        self.hotel = Hotel.objects.create(
            name='Test Hotel',
            address='Test Street',
            check_in_date='2025-06-13',
            check_out_date='2025-06-14',
        )
        ChecklistTask.objects.create(title='Test task', priority='high')

    def test_home_view(self):
        response = self.client.get(reverse('relay:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Conwy to Llanrwst')

    def test_stage_detail_view(self):
        response = self.client.get(reverse('relay:stage_detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Conwy to Llanrwst')

    def test_stage_detail_404(self):
        response = self.client.get(reverse('relay:stage_detail', args=[99]))
        self.assertEqual(response.status_code, 404)

    def test_team_roster_view(self):
        response = self.client.get(reverse('relay:team_roster'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dylan Lewis')

    def test_accommodation_view(self):
        response = self.client.get(reverse('relay:accommodation'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Hotel')

    def test_checklist_view(self):
        response = self.client.get(reverse('relay:checklist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test task')
