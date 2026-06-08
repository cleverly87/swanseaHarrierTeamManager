import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (
    Athlete, SupportStaff, Stage, Hotel, HotelRoom, HotelBooking, ChecklistTask, MediaUpload
)


def export_athletes_csv(modeladmin, request, queryset):
    """Export selected athletes to CSV with First Name, Surname, DOB, URN"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="athletes_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['First Name', 'Surname', 'Date of Birth', 'URN'])
    
    for athlete in queryset.order_by('last_name', 'first_name'):
        dob = athlete.date_of_birth.strftime('%d/%m/%Y') if athlete.date_of_birth else ''
        writer.writerow([
            athlete.first_name,
            athlete.last_name,
            dob,
            athlete.urn
        ])
    
    return response

export_athletes_csv.short_description = 'Export selected athletes to CSV (Name, DOB, URN)'


@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'date_of_birth', 'availability', 'is_reserve', 'urn', 'email', 'phone', 'assigned_stages')
    list_editable = ('availability', 'is_reserve')
    search_fields = ('first_name', 'last_name', 'email', 'urn')
    list_filter = ('is_reserve', 'availability')
    actions = [export_athletes_csv]
    ordering = ('last_name', 'first_name')
    fieldsets = (
        ('Personal Details', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'availability', 'is_reserve', 'urn', 'email', 'phone')
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
    search_fields = ('first_name', 'last_name', 'email')


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
        'start_time', 'athlete_report_time', 'athlete', 'stage_contact', 'start_location_name'
    )
    list_filter = ('day', 'is_mountain', 'athlete')
    search_fields = ('name', 'start_location_name', 'end_location_name', 'stage_number')
    autocomplete_fields = ['athlete', 'stage_contact']
    list_editable = ('athlete', 'stage_contact')
    ordering = ('stage_number',)
    fieldsets = (
        ('Stage Identity', {
            'fields': ('stage_number', 'name', 'day', 'distance_miles', 'is_mountain', 'description')
        }),
        ('Timing', {
            'fields': ('start_time', 'athlete_report_time')
        }),
        ('Stage Records', {
            'fields': (
                ('mens_record', 'mens_record_year'),
                ('womens_record', 'womens_record_year')
            ),
            'classes': ('collapse',),
        }),
        ('Locations', {
            'fields': (
                'start_location_name', 'start_location_address',
                'end_location_name', 'end_location_address',
                'travel_time_from_swansea'
            )
        }),
        ('Assignments', {
            'fields': ('athlete', 'stage_contact')
        }),
    )

    def display_distance_km(self, obj):
        return f"{obj.distance_km:.2f} km"
    display_distance_km.short_description = 'Distance (km)'

    def stage_type_badge(self, obj):
        if obj.is_mountain:
            return mark_safe('<span style="color:#c0392b;font-weight:bold;">⛰ Mountain</span>')
        return mark_safe('<span style="color:#27ae60;">🛣 Road</span>')
    stage_type_badge.short_description = 'Type'

    class Media:
        css = {
            'all': ('css/admin-custom.css',)
        }


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


@admin.register(MediaUpload)
class MediaUploadAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'title_or_filename', 'athlete', 'stage', 'uploaded_at', 'display_order', 'file_type')
    list_editable = ('display_order',)
    list_filter = ('stage', 'athlete', 'uploaded_at')
    search_fields = ('title', 'caption', 'athlete__first_name', 'athlete__last_name')
    date_hierarchy = 'uploaded_at'
    ordering = ['display_order', '-uploaded_at']
    
    fieldsets = (
        ('Media File', {
            'fields': ('file', 'file_preview')
        }),
        ('Details', {
            'fields': ('title', 'caption', 'athlete', 'stage'),
            'description': 'Add title, caption, and tag which athlete and stage this media is from.'
        }),
        ('Display Order', {
            'fields': ('display_order',),
            'description': 'Lower numbers appear first in the gallery (0, 1, 2, etc). Change this to reorder items.'
        }),
    )
    
    readonly_fields = ('file_preview', 'uploaded_at')
    
    # Use regular dropdowns instead of autocomplete for easier selection
    raw_id_fields = []
    
    def thumbnail_preview(self, obj):
        """Show small thumbnail in list view."""
        if not obj.file:
            return '—'
        try:
            if obj.is_image:
                return format_html(
                    '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 4px;" />',
                    obj.file.url
                )
            elif obj.is_video:
                return mark_safe('<span style="font-size: 2rem;">🎥</span>')
            return mark_safe('<span style="font-size: 2rem;">📎</span>')
        except:
            return '—'
    thumbnail_preview.short_description = 'Preview'
    
    def file_preview(self, obj):
        """Show larger preview in detail view."""
        if not obj.file:
            return '—'
        try:
            if obj.is_image:
                return format_html(
                    '<img src="{}" style="max-width: 400px; max-height: 400px; border-radius: 8px;" />',
                    obj.file.url
                )
            elif obj.is_video:
                return format_html(
                    '<video controls style="max-width: 400px; max-height: 400px;"><source src="{}" type="video/mp4"></video>',
                    obj.file.url
                )
            return format_html('<a href="{}" target="_blank">View File</a>', obj.file.url)
        except:
            return '—'
    file_preview.short_description = 'File Preview'
    
    def title_or_filename(self, obj):
        """Display title if set, otherwise filename."""
        if not obj:
            return '—'
        if obj.title:
            return obj.title
        if obj.file:
            try:
                return obj.file.name.split('/')[-1]
            except:
                return '—'
        return '—'
    title_or_filename.short_description = 'Title/Filename'
    
    def file_type(self, obj):
        """Show file type badge."""
        if not obj or not obj.file:
            return '—'
        try:
            if obj.is_image:
                return mark_safe('<span style="color: #27ae60; font-weight: bold;">🖼 Image</span>')
            elif obj.is_video:
                return mark_safe('<span style="color: #3498db; font-weight: bold;">🎥 Video</span>')
            return mark_safe('<span style="color: #95a5a6;">📎 File</span>')
        except:
            return '—'
    file_type.short_description = 'Type'
