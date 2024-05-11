from django.http.response import HttpResponse
from django.conf import settings
from django.shortcuts import render
from django.contrib.staticfiles import finders
from django.http import HttpResponseNotFound

# Create your views here.
def index(request):
    return HttpResponse("homepage")


def template_view(request, template_name):
    try:
        return render(request, template_name)
    except:
        return HttpResponseNotFound("Template not found")

def static_view(request, path):
    try:
        with open(f'my_app/static/{path}', 'rb') as f:
            return HttpResponse(f.read(), content_type='application/octet-stream')
    except FileNotFoundError:
        return HttpResponseNotFound("Static file not found")
