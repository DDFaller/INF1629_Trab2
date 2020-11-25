from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
#!/usr/bin/env python
import sys, os, string
from . import forms
from . import functions

def index(request):

    return render(request,"base.html")

def upload(request):
    if request.method == 'POST':
        #if 'document' in request.FILES:
        fs = FileSystemStorage()

        context = {}
        uploadedFile = request.FILES['document']
        stopwordsFile = request.FILES['stopwords']
        fs.save( uploadedFile.name, uploadedFile )
        fs.save( stopwordsFile.name, stopwordsFile )
        termFrequency = term_frequency_calculator(uploadedFile.name, stopwordsFile.name)
        termFrequency.generate_frequency_file()
        frequenciesList = termFrequency.show_top25()
        context['worddict'] = frequenciesList
        return render(request, 'uploadedView.html',context)
    return render(request,'upload.html')


    # Utility for handling the intermediate 'secondary memory'


class term_frequency_calculator():
    def __init__(self,stopwords_file,content_file):
        self.stopwords = open( 'media/' + stopwords_file, 'r')
        self.word_freqs = {}
        self.content_file = 'media/' + content_file
    #Recebe um arquivo e iterando suas linhas registra as frequências das palavras
    #num segundo arquivo.
    #PRE: data_file possui conteudo a ser contabilizado(Verificação: existe uma assertiva garantindo isto)
    #POS: foi criado um arquivo a partir do data_file, onde as palavras não contidas no arquivo de stopwords
    #terão suas frequências armazenadas. Não é possível modificar o arquivo de stopwords dentro
    #da aplicação.
    #Palavras compostas ou que possuam caracteres especiais serão divididas e armazenadas separadamente.
    def generate_frequency_file(self):
        line = []
        word = ""
        data_file = open(self.content_file, 'r')
        lines = self.data_file.read().split("\n")
        for line in lines:
            print("Show line -> " + line)
            line_split = line.split(" ")
            for word in line_split:
                if len(word) >= 2 and word:
                    # Checa se palavra já foi guardada
                    if word in self.word_freqs.keys():
                        self.word_freqs[word] += 1
                    else:
                        self.word_freqs[word] = 1



    #Recebe um arquivo cpm as frequências de cada palavra.
    #PRE: word_freqs possui conteudo a ser classificado(Verificação: existe uma assertiva garantindo isto)
    #POS: foi criada uma lista em memória a partir do word_freqs, onde os 25 primeiros elementos desta lista
    #correspondem as top 25 palavras com maior frequência.
    #Duas palavras com a mesma frequência irão aparecer de acordo com sua ocorrência no arquivo.
    def show_top25(self):
        return str(self.word_freqs)
