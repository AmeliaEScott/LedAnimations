from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .LedsBackend.led_supervisor import LedSupervisor
import json


# This code is run when Django starts up
# I don't know if it's good practice to put code here, but hey, it works
print("Initializing led_supervisor...")
# The LED Supervisor handles all of the animations, and has them do their thing ~30 times per second
ledSupervisor = LedSupervisor()
print("Done initializing LED supervisor.")


def index(request):
    context = {
        'animationoptionsjson': json.dumps(ledSupervisor.getanimationoptions()),
        'animationoptions': ledSupervisor.getanimationoptions()
    }
    # ledSupervisor.addanimation('Fairy', {'start': 1, 'width': 5, 'speed': 2, 'color': (255, 0, 0)})
    return HttpResponse(render(context=context, request=request, template_name='LedsApp/index.html'))
    # return HttpResponse(repr(ledSupervisor.getanimationoptions()))


def getanimationoptions(request):
    return JsonResponse(ledSupervisor.getanimationoptions())


def getanimations(request):
    animations = ledSupervisor.getanimations()
    output = {}
    for id in animations:
        output[id] = {
            "name": animations[id].getanimationinfo()['name'],
            "options": animations[id].options
        }
    return JsonResponse(output)


@csrf_exempt
def addanimation(request):
    if request.method.lower() != "post":
        return HttpResponse("Method not supported. Must use POST.", status=403)

    # try:
    data = json.loads(request.body.decode("utf-8"))
    animationdata = data['data']
    name = data['name']
    # except:
    #     return HttpResponse("Could not load animation data", status=404)
    ledSupervisor.addanimation(name, animationdata)
    return HttpResponse("Successfully added animation.", status=200)


@csrf_exempt
def removeanimation(request, id):
    if request.method.lower() == "delete":
        ledSupervisor.removeanimation(int(id))
        return HttpResponse("Successfully deleted animation.", status=200)
    else:
        return HttpResponse("Method not supported. Must use DELETE", status=403)
