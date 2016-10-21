from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .LedsBackend.led_supervisor import LedSupervisor
import json

print("Initializing led_supervisor...")
ledSupervisor = LedSupervisor()
print("Done initializing LED supervisor.")


def index(request):
    context = {
        'animationoptionsjson': json.dumps(ledSupervisor.getanimationoptions()),
        'animationoptions': ledSupervisor.getanimationoptions()
    }
    return HttpResponse(render(context=context, request=request, template_name='LedsApp/index.html'))
    # return HttpResponse(repr(ledSupervisor.getanimationoptions()))


def getanimations(request):
    pass
