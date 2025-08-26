"""
URLs for dashboard app.
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='home'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
]