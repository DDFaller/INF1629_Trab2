from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

def index(request):
    return HttpResponse("Hello, World!")

def upload(request):
    return render(request,'main/upload.html')
