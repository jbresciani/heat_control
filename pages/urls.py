from .views import home_view, thermostatsControlView
from django.urls import path

urlpatterns = [
    path('', home_view, name='Home'),
    path('thermostats_control/', thermostatsControlView.as_view()),
    # path('thermostats_control/', thermostats_control_view, name='metrics')
]
