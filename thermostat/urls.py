from .views import thermostatRestView
from django.urls import path

urlpatterns = [
    path('rest/', thermostatRestView.as_view()),
]
