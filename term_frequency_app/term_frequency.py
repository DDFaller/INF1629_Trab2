#!/usr/bin/env python
import sys, os, string

# Utility for handling the intermediate 'secondary memory'


class term_frequency_calculator():
    def __init__(self,stopwords_file,content_file):
        self.stopwords_file = stopwords_file.open()#'../stop_words.txt'
        self.stopwords = self.stopwords_file.read().split(',')
        print('====================================')
        print(self.stopwords)
        self.stopwords_file.close()
        self.word_freqs = self.touchopen('word_freqs', 'rb+')
        self.data_file = content_file.open()


    def touchopen(filename, *args, **kwargs):
        try:
            os.remove(filename)
        except OSError:
            pass
        open(filename, "a").close() # "touch" file
        return open(filename, *args, **kwargs)

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
        is_found = False
        word = ""
        stored_word = ""
        frequency = 0


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
                        is_found = False
                        word = line[0][word_start:word_index].lower()
                        if len(word) >= 2 and not (word in self.stopwords):
                            # Checa se palavra já foi guardada
                            while True:
                                stored_word = str(self.word_freqs.readline().strip(), 'utf-8')
                                if stored_word == '':
                                    break;
                                frequency = int(stored_word.split(',')[1])
                                stored_word = stored_word.split(',')[0].strip()
                                if word == stored_word:
                                    frequency += 1
                                    is_found = True
                                    break
                            if not is_found:
                                self.word_freqs.seek(0, 1)
                                self.word_freqs.write(bytes("%20s,%04d\n" % (word, 1), 'utf-8'))
                            else:
                                self.word_freqs.seek(-26, 1)
                                self.word_freqs.write(bytes("%20s,%04d\n" % (word, frequency), 'utf-8'))
                            self.word_freqs.seek(0,0)
                        word_start = None
                word_index += 1
        self.data_file.close()
        self.word_freqs.flush()



    #Recebe um arquivo cpm as frequências de cada palavra.
    #PRE: word_freqs possui conteudo a ser classificado(Verificação: existe uma assertiva garantindo isto)
    #POS: foi criada uma lista em memória a partir do word_freqs, onde os 25 primeiros elementos desta lista
    #correspondem as top 25 palavras com maior frequência.
    #Duas palavras com a mesma frequência irão aparecer de acordo com sua ocorrência no arquivo.
    def show_top25(self):
        top_frequencies = []
        current_word = ""
        frequency = 0

        while True:
            line = str(self.word_freqs.readline().strip(), 'utf-8')
            if line == '': # EOF
                break
            frequency = int(line.split(',')[1]) #Obtem frequencia
            current_word = line.split(',')[0].strip() #Obtem palavra

            # Checa se palavra já foi classificada
            for index in range(25):
                if index > len(top_frequencies) - 1:
                    top_frequencies.append([current_word, frequency])
                    break
                if top_frequencies[index] == [] or top_frequencies[index][1] < frequency:
                    top_frequencies.insert(index, [current_word, frequency])
                    frequency = 0
                    break

        #for tf in top_frequencies:
            #if len(tf) == 2:
            #    print(tf[0], '-', tf[1])
        self.word_freqs.close()
        return top_frequencies
