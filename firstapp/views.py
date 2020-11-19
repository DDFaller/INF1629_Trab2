from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

def index(request):
    return render(request,"base.html")

def upload(request):
    return render(request,'upload.html')
