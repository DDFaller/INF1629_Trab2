from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
#!/usr/bin/env python
import sys, os, string
from . import forms
from . import functions

def index(request):

    return render(request,"base.html")

def upload(request):
    if request.method == 'POST':
        #if 'document' in request.FILES:
        context = {}
        uploadedFile = request.FILES['document']
        stopwordsFile = request.FILES['stopwords']
        termFrequency = term_frequency_calculator(uploadedFile,stopwordsFile)
        termFrequency.generate_frequency_file()
        frequenciesList = termFrequency.show_top25()
        context['worddict'] = frequenciesList
        return render(request, 'uploadedView.html',context)
    return render(request,'upload.html')


    # Utility for handling the intermediate 'secondary memory'


class term_frequency_calculator():
    def __init__(self,stopwords_file,content_file):
        self.stopwords = stopwords_file.open()#'../stop_words.txt'
        self.word_freqs = {}
        self.data_file = content_file.open()

    #Recebe um arquivo e iterando suas linhas registra as frequências das palavras
    #num segundo arquivo.
    #PRE: data_file possui conteudo a ser contabilizado(Verificação: existe uma assertiva garantindo isto)
    #POS: foi criado um arquivo a partir do data_file, onde as palavras não contidas no arquivo de stopwords
    #terão suas frequências armazenadas. Não é possível modificar o arquivo de stopwords dentro
    #da aplicação.
    #Palavras compostas ou que possuam caracteres especiais serão divididas e armazenadas separadamente.
    def generate_frequency_file(self):
        line = []
        word_start = 0
        word_index = 0
        word = ""


        while True:
            line = [self.data_file.readline()]
            if line == ['']: # Verificação de fim do arquivo
                break
            if line[0][len(line[0])-1] != '\n':
                line[0] = line[0] + '\n'
            word_start = None
            word_index = 0

            #Iterar cada caracter na linha
            for c in line[0]:
                if word_start == None:
                    if c.isalnum():
                        #Ínicio de palavra
                        word_start = word_index
                #Conhecemos a palavra
                else:
                    if not c.isalnum():
                        word = line[0][word_start:word_index].lower()
                        if len(word) >= 2 and word not in self.stopwords:
                            # Checa se palavra já foi guardada
                            if word in self.word_freqs.keys():
                                self.word_freqs[word] += 1
                            else:
                                self.word_freqs[word] = 1
                        word_start = None
                word_index += 1



    #Recebe um arquivo cpm as frequências de cada palavra.
    #PRE: word_freqs possui conteudo a ser classificado(Verificação: existe uma assertiva garantindo isto)
    #POS: foi criada uma lista em memória a partir do word_freqs, onde os 25 primeiros elementos desta lista
    #correspondem as top 25 palavras com maior frequência.
    #Duas palavras com a mesma frequência irão aparecer de acordo com sua ocorrência no arquivo.
    def show_top25(self):
        top_frequencies = {}
        sort_orders = sorted(self.word_freqs.items(), key=lambda x: x[1], reverse=True)

        count = 0
        for k,v in sort_orders.items():
            top_frequencies[k] = v
            count += 1

        return top_frequencies
