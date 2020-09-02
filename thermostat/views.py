from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

# Create your views here.
mock_thermostat = {'current_temp': 1}

class thermostatRestView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(thermostatRestView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        global mock_thermostat
        return JsonResponse({'current_temp': mock_thermostat['current_temp']})

    def post(self, request):
        global mock_thermostat
        payload = json.loads(request.body)
        mock_thermostat['current_temp'] = int(payload['requested_temp'])
        return HttpResponse("OK")
