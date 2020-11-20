from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from forms import FileFieldForm
from functions import handle_uploaded_file

def index(request):

    return render(request,"base.html")

def formSubmission(request):
    form = FileFieldForm()
    if request.method == "POST":
        form = FileFieldForm(request.POST,request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse("File uploaded sucessfully")
        else:
            form = FileFieldForm()
    return render(request,'home.html',{'form': form})
    #return render(request,'upload.html')
