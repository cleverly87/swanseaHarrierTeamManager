from django.db import models


class Athlete(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    urn = models.CharField(max_length=50, blank=True, verbose_name='URN')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=30, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class SupportStaff(models.Model):
    ROLE_CHOICES = [
        ('driver', 'Driver'),
        ('medic', 'Medic'),
        ('manager', 'Team Manager'),
        ('coordinator', 'Coordinator'),
        ('photographer', 'Photographer'),
        ('other', 'Other'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='other')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name_plural = 'Support Staff'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Stage(models.Model):
    DAY_CHOICES = [
        (1, 'Day 1'),
        (2, 'Day 2'),
    ]
    stage_number = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=200)
    day = models.IntegerField(choices=DAY_CHOICES, default=1)
    distance_miles = models.DecimalField(max_digits=6, decimal_places=2, help_text='Distance in miles')
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, help_text='Distance in kilometres (auto-calculated)', editable=False)
    is_mountain = models.BooleanField(default=False, help_text='Tick if this is a mountain stage')
    description = models.TextField(blank=True)

    # Timing
    start_time = models.TimeField(null=True, blank=True, help_text='Scheduled start time of the stage')
    athlete_report_time = models.TimeField(null=True, blank=True, help_text='When the athlete must be at the start')

    # Location
    start_location_name = models.CharField(max_length=200, blank=True)
    start_location_address = models.TextField(blank=True, help_text='Full postal address of the start point')
    end_location_name = models.CharField(max_length=200, blank=True)
    end_location_address = models.TextField(blank=True)

    # Assigned athlete
    athlete = models.ForeignKey(
        Athlete,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='stages',
    )

    class Meta:
        ordering = ['stage_number']

    def save(self, *args, **kwargs):
        # Auto-convert miles to km (1 mile = 1.60934 km)
        if self.distance_miles:
            self.distance_km = self.distance_miles * 1.60934
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Stage {self.stage_number}: {self.name}"

    @property
    def stage_type_label(self):
        return 'Mountain' if self.is_mountain else 'Road'


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    total_rooms_booked = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class HotelRoom(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('twin', 'Twin'),
        ('triple', 'Triple'),
        ('family', 'Family'),
    ]
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_identifier = models.CharField(max_length=50, help_text='Room number or name, e.g. 101 or "Blue Room"')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='twin')
    capacity = models.PositiveIntegerField(default=2)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['hotel', 'room_identifier']
        unique_together = [['hotel', 'room_identifier']]

    def __str__(self):
        return f"{self.hotel.name} – Room {self.room_identifier} ({self.get_room_type_display()})"


class HotelBooking(models.Model):
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, related_name='bookings')
    athlete = models.ForeignKey(
        Athlete, null=True, blank=True, on_delete=models.SET_NULL, related_name='hotel_bookings'
    )
    support_staff = models.ForeignKey(
        SupportStaff, null=True, blank=True, on_delete=models.SET_NULL, related_name='hotel_bookings'
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['room']

    def __str__(self):
        person = self.athlete or self.support_staff
        return f"{person} → {self.room}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.athlete and not self.support_staff:
            raise ValidationError('A booking must be linked to either an athlete or support staff member.')
        if self.athlete and self.support_staff:
            raise ValidationError('A booking cannot be linked to both an athlete and support staff – choose one.')


class ChecklistTask(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    assigned_to = models.CharField(max_length=100, blank=True, help_text='Name of person responsible')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['completed', 'due_date', 'priority']
        verbose_name = 'Checklist Task'
        verbose_name_plural = 'Checklist Tasks'

    def __str__(self):
        status = '✓' if self.completed else '○'
        return f"[{status}] {self.title}"
