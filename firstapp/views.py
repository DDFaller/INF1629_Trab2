from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from . import forms
from . import functions
import term_frequency from term_frequency.py
import touchopen from term_frequency.py

def index(request):

    return render(request,"base.html")

def upload(request):
    if request.method == 'POST':
        #if 'document' in request.FILES:
        context = {}
        uploadedFile = request.FILES['document']
        stopwordsFile = request.FILES['stopwords']
        termFrequency = term_frequency(uploadedFile,stopwordsFile)
        termFrequency.generate_frequency_file()
        frequenciesList = termFrequency.show_top25()
        context['worddict'] = frequenciesList
        return render(request, 'uploadedView.html',context)
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
