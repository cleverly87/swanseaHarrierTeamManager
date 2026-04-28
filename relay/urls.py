from django.urls import path
from . import views

app_name = 'relay'

urlpatterns = [
    path('', views.relay_home, name='home'),
    path('stage/<int:stage_number>/', views.stage_detail, name='stage_detail'),
    path('team/', views.team_roster, name='team_roster'),
    path('accommodation/', views.accommodation_summary, name='accommodation'),
    path('checklist/', views.checklist_view, name='checklist'),
]
