from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from . import forms
from . import functions

def index(request):

    return render(request,"base.html")

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        return render(request, 'uploadedView.html')
    return render(request,'upload.html')


#def get(request):
#    context = RequestContext(request)
#    context_dict = {}
#    # Key statement needs to be added
#    context_dict.update(csrf(request))
#    return render_to_response("upload.html", context_dict, context)

#def formSubmission(request):
#    form = forms.FileFieldForm()
#    if request.method == "POST":
#        form = forms.FileFieldForm(request.POST,request.FILES)
#        if form.is_valid():
#            functions.handle_uploaded_file(request.FILES['file'])
#            return HttpResponse("File uploaded sucessfully")
#        else:
#            form = forms.FileFieldForm()
#    return render(request,'home.html',{'form': form})
    #return render(request,'upload.html')
