from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from LedsBackend import led_supervisor

print("WOW, VERY MUCH OF THE TESTING IS BEING DONE")
#led_supervisor.test()


def index(request):
    return HttpResponse(render(request=request, template_name='LedsApp/index.html'))
