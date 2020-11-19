from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, World!")

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        print(uploaded_file.name)
        print(uploaded_file.size)
    return render(request, 'upload.html')
# Create your views here.
