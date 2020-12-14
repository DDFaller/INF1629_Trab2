from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
#!/usr/bin/env python
import sys, os, string
from . import forms
from . import functions

def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")


def upload(request):
    if request.method == 'POST':
        #if 'document' in request.FILES:
        fs = FileSystemStorage()

        context = {}
        uploadedFile = request.FILES['document']
        stopwordsFile = request.FILES['stopwords']
        if not ('document' in request.FILES) or not ('stopwords' in request.FILES):
            return render(request,'uploadFail.html')
        fs.save( uploadedFile.name, uploadedFile )
        fs.save( stopwordsFile.name, stopwordsFile )
        termFrequency = term_frequency_calculator(stopwordsFile.name,uploadedFile.name)
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
        lines = data_file.read().split("\n")

        for line in lines:
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
        top_frequencies = {k: v for k, v in sorted(self.word_freqs.items(), key=lambda item: item[1])}

        top_frequencies_values = list(top_frequencies.values())[::-1]
        top_frequencies_keys = list(top_frequencies.keys())[::-1]

        new_top_frequencies = {}
        for i in range(0,25):
            if i == len(top_frequencies.keys()):
                break
            new_top_frequencies[top_frequencies_keys[i]] = top_frequencies_values[i]

        return new_top_frequencies
