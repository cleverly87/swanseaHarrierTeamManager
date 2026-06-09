from django.shortcuts import render, get_object_or_404
from django.db import models
from .models import Stage, Athlete, SupportStaff, Hotel, HotelRoom, ChecklistTask


def relay_home(request):
    """Public home page – relay overview with all stages."""
    day1_stages = Stage.objects.filter(day=1).select_related('athlete')
    day2_stages = Stage.objects.filter(day=2).select_related('athlete')
    total_stages = Stage.objects.count()
    athletes_assigned = Stage.objects.filter(athlete__isnull=False).values('athlete').distinct().count()
    
    # Get all reserve athletes
    reserves = Athlete.objects.filter(is_reserve=True).order_by('last_name', 'first_name')
    
    context = {
        'day1_stages': day1_stages,
        'day2_stages': day2_stages,
        'total_stages': total_stages,
        'athletes_assigned': athletes_assigned,
        'reserves': reserves,
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
                default='min_stage',
                output_field=models.IntegerField()
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


def marshalling_view(request):
    """Swansea Harriers marshalling duties for Stage 14."""
    return render(request, 'relay/marshalling.html')


def gallery_view(request):
    """Photo and video gallery from the event."""
    from .models import MediaUpload
    
    # Get all media uploads
    all_media = MediaUpload.objects.all().order_by('display_order', '-uploaded_at')
    
    # Separate into photos and videos using the media_type field
    photos = [m for m in all_media if m.media_type == 'image']
    videos = [m for m in all_media if m.media_type == 'video']
    
    context = {
        'photos': photos,
        'videos': videos,
        'total_count': len(photos) + len(videos)
    }
    return render(request, 'relay/gallery.html', context)


def upload_media(request):
    """Allow athletes to upload photos and videos (bulk upload supported)."""
    from django.shortcuts import redirect
    from django.contrib import messages
    from django.http import JsonResponse
    from .models import MediaUpload
    import json
    
    if request.method == 'POST':
        # Check if it's a bulk upload (AJAX)
        file_count = request.POST.get('file_count')
        
        if file_count:
            try:
                count = int(file_count)
                uploaded = 0
                errors = []
                
                for i in range(count):
                    file = request.FILES.get(f'file_{i}')
                    title = request.POST.get(f'title_{i}', '')
                    caption = request.POST.get(f'caption_{i}', '')
                    
                    if file:
                        try:
                            MediaUpload.objects.create(
                                file=file,
                                title=title,
                                caption=caption
                            )
                            uploaded += 1
                        except Exception as e:
                            errors.append(f"File {i}: {str(e)}")
                
                if uploaded > 0:
                    return JsonResponse({
                        'success': True,
                        'message': f'{uploaded} file(s) uploaded successfully!',
                        'errors': errors if errors else None
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'No files were uploaded. ' + ('; '.join(errors) if errors else '')
                    }, status=400)
                    
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': f'Upload error: {str(e)}'
                }, status=400)
        
        # Single file upload (fallback) - for non-JavaScript uploads
        file = request.FILES.get('media_file')
        title = request.POST.get('title', '')
        caption = request.POST.get('caption', '')
        
        if file:
            try:
                MediaUpload.objects.create(
                    file=file,
                    title=title,
                    caption=caption
                )
                messages.success(request, 'Your media has been uploaded successfully!')
            except Exception as e:
                messages.error(request, f'Upload failed: {str(e)}')
            return redirect('relay:gallery')
        else:
            messages.error(request, 'Please select a file to upload.')
    
    athletes = Athlete.objects.all().order_by('last_name', 'first_name')
    stages = Stage.objects.all().order_by('stage_number')
    return render(request, 'relay/upload_media.html', {'athletes': athletes, 'stages': stages})


def save_cloudinary_upload(request):
    """Save Cloudinary upload URLs to database (for direct browser uploads)."""
    from django.http import JsonResponse
    from django.views.decorators.csrf import csrf_exempt
    from .models import MediaUpload
    from django.core.files.base import ContentFile
    import json
    import logging
    
    logger = logging.getLogger(__name__)
    
    # Note: This view is intentionally NOT decorated with @csrf_exempt
    # because we want CSRF protection, but we'll handle the token properly
    
    if request.method != 'POST':
        logger.warning(f"save_cloudinary_upload called with method: {request.method}")
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        logger.info(f"save_cloudinary_upload called. Content-Type: {request.content_type}")
        data = json.loads(request.body)
        uploads = data.get('uploads', [])
        
        print(f"DEBUG: Received {len(uploads)} uploads")
        logger.info(f"Received {len(uploads)} uploads")
        
        if not uploads:
            return JsonResponse({'error': 'No uploads provided'}, status=400)
        
        saved_count = 0
        for upload_data in uploads:
            cloudinary_url = upload_data.get('cloudinary_url')
            public_id = upload_data.get('cloudinary_public_id')
            title = upload_data.get('title', '')
            caption = upload_data.get('caption', '')
            file_type = upload_data.get('file_type', 'image')
            
            print(f"DEBUG: Processing upload - public_id: {public_id}, file_type: {file_type}")
            print(f"DEBUG: cloudinary_url: {cloudinary_url}")
            
            if not public_id:
                continue
            
            # The public_id should now include the folder path since we set it explicitly
            # But if it doesn't, extract from URL or construct it
            if 'welsh_castles_relay_2026' not in public_id:
                if cloudinary_url and 'welsh_castles_relay_2026' in cloudinary_url:
                    # Extract the path from the URL
                    import re
                    match = re.search(r'upload/v\d+/(.+?)(?:\.[^.]+)?$', cloudinary_url)
                    if match:
                        public_id = match.group(1)
                        print(f"DEBUG: Extracted from URL: {public_id}")
                else:
                    # Construct the path manually
                    folder = 'photos' if file_type == 'image' else 'videos'
                    public_id = f'welsh_castles_relay_2026/{folder}/{public_id}'
                    print(f"DEBUG: Constructed path: {public_id}")
            
            media = MediaUpload()
            media.file.name = public_id
            media.title = title
            media.caption = caption
            media.save()
            
            print(f"DEBUG: Saved with file.name: {media.file.name}")
            
            saved_count += 1
        
        logger.info(f"Successfully saved {saved_count} uploads")
        return JsonResponse({
            'success': True,
            'message': f'{saved_count} file(s) saved successfully!'
        })
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Save error: {str(e)}", exc_info=True)
        return JsonResponse({'error': f'Save error: {str(e)}'}, status=500)
