from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Athlete, SupportStaff, Stage, Hotel, HotelRoom, HotelBooking, ChecklistTask
)


@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'urn', 'email', 'phone', 'assigned_stages')
    search_fields = ('first_name', 'last_name', 'email', 'urn')
    fieldsets = (
        ('Personal Details', {
            'fields': ('first_name', 'last_name', 'urn', 'email', 'phone')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone'),
            'classes': ('collapse',),
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
    )

    def assigned_stages(self, obj):
        stages = obj.stages.all()
        if stages:
            return ', '.join(str(s) for s in stages)
        return '—'
    assigned_stages.short_description = 'Assigned Stages'


@admin.register(SupportStaff)
class SupportStaffAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role', 'email', 'phone')
    list_filter = ('role',)
    search_fields = ('first_name', 'last_name')


class HotelRoomInline(admin.TabularInline):
    model = HotelRoom
    extra = 1
    show_change_link = True


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'check_in_date', 'check_out_date', 'total_rooms_booked')
    inlines = [HotelRoomInline]
    fieldsets = (
        ('Hotel Details', {
            'fields': ('name', 'address', 'phone', 'email', 'website')
        }),
        ('Booking Dates', {
            'fields': ('check_in_date', 'check_out_date', 'total_rooms_booked')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
    )


class HotelBookingInline(admin.TabularInline):
    model = HotelBooking
    extra = 1


@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_identifier', 'room_type', 'capacity', 'occupants')
    list_filter = ('hotel', 'room_type')
    inlines = [HotelBookingInline]

    def occupants(self, obj):
        bookings = obj.bookings.all()
        names = []
        for b in bookings:
            if b.athlete:
                names.append(b.athlete.full_name)
            elif b.support_staff:
                names.append(b.support_staff.full_name)
        return ', '.join(names) if names else '—'
    occupants.short_description = 'Occupants'


@admin.register(HotelBooking)
class HotelBookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'person_name', 'person_type')
    list_filter = ('room__hotel',)

    def person_name(self, obj):
        if obj.athlete:
            return obj.athlete.full_name
        if obj.support_staff:
            return obj.support_staff.full_name
        return '—'
    person_name.short_description = 'Person'

    def person_type(self, obj):
        if obj.athlete:
            return 'Athlete'
        if obj.support_staff:
            return 'Support Staff'
        return '—'
    person_type.short_description = 'Type'


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = (
        'stage_number', 'name', 'day', 'distance_miles', 'display_distance_km', 'stage_type_badge',
        'start_time', 'athlete_report_time', 'athlete', 'start_location_name'
    )
    list_filter = ('day', 'is_mountain', 'athlete')
    search_fields = ('name', 'start_location_name', 'end_location_name')
    autocomplete_fields = ['athlete']
    list_editable = ('athlete',)
    fieldsets = (
        ('Stage Identity', {
            'fields': ('stage_number', 'name', 'day', 'distance_miles', 'is_mountain', 'description')
        }),
        ('Timing', {
            'fields': ('start_time', 'athlete_report_time')
        }),
        ('Locations', {
            'fields': (
                'start_location_name', 'start_location_address',
                'end_location_name', 'end_location_address'
            )
        }),
        ('Athlete Assignment', {
            'fields': ('athlete',)
        }),
    )

    def display_distance_km(self, obj):
        return f"{obj.distance_km:.2f} km"
    display_distance_km.short_description = 'Distance (km)'

    def stage_type_badge(self, obj):
        if obj.is_mountain:
            return format_html('<span style="color:#c0392b;font-weight:bold;">⛰ Mountain</span>')
        return format_html('<span style="color:#27ae60;">🛣 Road</span>')
    stage_type_badge.short_description = 'Type'


@admin.register(ChecklistTask)
class ChecklistTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'due_date', 'due_time', 'assigned_to', 'completed')
    list_filter = ('priority', 'completed', 'due_date')
    list_editable = ('completed', 'priority')
    search_fields = ('title', 'assigned_to')
    date_hierarchy = 'due_date'
    fieldsets = (
        ('Task', {
            'fields': ('title', 'description', 'priority', 'assigned_to')
        }),
        ('Due Date & Time', {
            'fields': ('due_date', 'due_time')
        }),
        ('Status', {
            'fields': ('completed', 'completed_at')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
    )
