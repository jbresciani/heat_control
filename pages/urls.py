from .views import home_view, thermostats_control_view
from django.urls import path

urlpatterns = [
    path('', home_view, name='Home'),
    path('thermostats_control/', thermostats_control_view, name='metrics')
]
