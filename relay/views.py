from django.shortcuts import render, get_object_or_404
from django.db import models
from .models import Stage, Athlete, SupportStaff, Hotel, HotelRoom, ChecklistTask


def relay_home(request):
    """Public home page – relay overview with all stages."""
    day1_stages = Stage.objects.filter(day=1).select_related('athlete')
    day2_stages = Stage.objects.filter(day=2).select_related('athlete')
    total_stages = Stage.objects.count()
    athletes_assigned = Stage.objects.filter(athlete__isnull=False).values('athlete').distinct().count()
    context = {
        'day1_stages': day1_stages,
        'day2_stages': day2_stages,
        'total_stages': total_stages,
        'athletes_assigned': athletes_assigned,
    }
    return render(request, 'relay/home.html', context)


def stage_detail(request, stage_number):
    """Public page for a single stage."""
    stage = get_object_or_404(Stage, stage_number=stage_number)
    context = {'stage': stage}
    return render(request, 'relay/stage_detail.html', context)


def team_roster(request):
    """Public page listing all athletes in the squad."""
    sort = request.GET.get('sort', 'name')  # Default sort by name
    
    athletes = Athlete.objects.prefetch_related('stages')
    
    if sort == 'stage':
        # Sort by stage number (athletes with stages first, then by lowest stage number)
        athletes = athletes.annotate(
            min_stage=models.Min('stages__stage_number')
        ).order_by(
            models.Case(
                models.When(min_stage__isnull=True, then=999),
                default='min_stage'
            )
        )
    else:  # sort == 'name' (default)
        athletes = athletes.order_by('last_name', 'first_name')
    
    context = {
        'athletes': athletes,
        'current_sort': sort,
    }
    return render(request, 'relay/team_roster.html', context)


def accommodation_summary(request):
    """Public-facing accommodation summary."""
    hotels = Hotel.objects.prefetch_related('rooms__bookings__athlete', 'rooms__bookings__support_staff')
    context = {'hotels': hotels}
    return render(request, 'relay/accommodation.html', context)


def checklist_view(request):
    """Public view of the team manager checklist."""
    tasks_incomplete = ChecklistTask.objects.filter(completed=False)
    tasks_complete = ChecklistTask.objects.filter(completed=True)
    context = {
        'tasks_incomplete': tasks_incomplete,
        'tasks_complete': tasks_complete,
    }
    return render(request, 'relay/checklist.html', context)
