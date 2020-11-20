from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from . import forms
from . import functions

def index(request):

    return render(request,"base.html")

def formSubmission(request):
    form = forms.FileFieldForm()
    if request.method == "POST":
        form = forms.FileFieldForm(request.POST,request.FILES)
        if form.is_valid():
            functions.handle_uploaded_file(request.FILES['file'])
            return HttpResponse("File uploaded sucessfully")
        else:
            form = forms.FileFieldForm()
    return render(request,'home.html',{'form': form})
    #return render(request,'upload.html')
