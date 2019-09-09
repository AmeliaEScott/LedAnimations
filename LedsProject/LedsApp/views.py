from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .LedsBackend.led_supervisor import LedSupervisor
from .LedsBackend.animation import animation_classes
import json


# This code is run when Django starts up
# I don't know if it's good practice to put code here, but hey, it works
print("Initializing led_supervisor...")
# The LED Supervisor handles all of the animations, and has them do their thing ~30 times per second
ledSupervisor = LedSupervisor()
print("Done initializing LED supervisor.")


def index(request, error=None):
    print("CURRENT ANIMATIONS:")
    print(ledSupervisor.getanimationsjson())

    context = {
        'animationoptions': ledSupervisor.getanimationoptions(),
        'animations': ledSupervisor.getanimationsjson(),
        'error': error
    }

    return HttpResponse(render(context=context, request=request, template_name='LedsApp/indexv2.html'))


def addanimation(request):
    error = None
    if request.method == "POST":
        form_data = dict(request.POST.copy())
        animation_name = next(iter(form_data['animation_name']))
        del form_data['animation_name']
        del form_data['csrfmiddlewaretoken']

        animation_data = {
            name: next(iter(value)) for name, value in form_data.items()
        }

        try:
            ledSupervisor.addanimation(animation_name, animation_data)
        except Exception as e:
            error = str(e)

        # TODO: How to show the error
        # Use session: https://docs.djangoproject.com/en/2.2/topics/http/sessions/
        return redirect("index")
    else:
        return HttpResponse("Method not supported. Should use POST.", 405)


@csrf_exempt
def removeanimation(request):
    if request.method.lower() == "post":
        id = next(iter(request.POST['id']))
        ledSupervisor.removeanimation(int(id))
        # TODO: Possible error code, probably using session
        return redirect("index")
    else:
        return HttpResponse("Method not supported. Must use POST. You used {}".format(request.method), status=403)
