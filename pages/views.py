from django.shortcuts import render, redirect

def home_view(requests):
    return redirect('thermostats_control/', permanent=False)

def get_thermostats():
    return [{
        "id": "123451234",
        "name": "mockunit",
        "group": "mockgroup",
        "description": "mock",
        "url": "http://localhost:1234",
        "requested_temp": 10
    }]

def thermostats_control_view(request):
    context = {
        "groups": ["mockgroup"],
        "thermostats": get_thermostats()
    }
    return render(request, 'thermostats_control.html', context)
