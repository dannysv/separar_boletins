import textract 
import codecs
import os
import re 

def decide_word(words, lines_pdf):
    l_linespdf = ''.join(lines_pdf)
    #l_ocurrs = []
    index = -1
    max_ = 0
    word_ = ''
    for i, word in enumerate(words):
        ocurrs = re.findall(word, l_linespdf)
        #print(ocurrs)
        if len(ocurrs)> max_:
            max_ = len(ocurrs)
            index = i
            word_ = word 
    return (index, max_, word_)

def get_keyword_pten(lines_pdf, minim):
    guide_words = ['Resumo\n', 'resumo\n', 'RESUMO\n', 'Resumo -','RESUMO -', '<-->RESUMO']
    (i, max_, w) = decide_word(guide_words, lines_pdf)
    #minim = 3
    print("=== Key word ===")
    if max_<minim:
        guide_words = ['Sinopse\n', 'sinopse\n', 'SINOPSE\n', 'Sinopse -','SINOPSE -', '<-->SINOPSE']
        (i, max_, w) = decide_word(guide_words, lines_pdf)
        if max_<minim:
            guide_words = ['Introdução\n', 'introdução\n', 'INTRODUÇÃO\n', 'Introdução -', 'INTRODUÇÃO -', '<-->INTRODUÇÃO']
            (i, max_, w) = decide_word(guide_words, lines_pdf)
            if max_<minim:
                guide_words = ['Introduction\n', 'introduction\n', 'INTRODUCTION\n', 'Introduction -', '<-->INTRODUCTION -', 'INTRODUCTION']
                (i, max_, w) = decide_word(guide_words, lines_pdf)
                if max_<minim:
                    guide_words = ['Abstract\n', 'abstract\n', 'ABSTRACT\n', 'Abstract -', 'ABSTRACT -', '<-->ABSTRACT']
                    (i, max_, w) = decide_word(guide_words, lines_pdf)
                    if max_<minim:
                        guide_words = ['Diagnosis\n', 'diagnosis\n', 'DIAGNOSIS\n', 'Diagnosis -','DIAGNOSIS -', '<-->DIAGNOSIS']
                        (i, max_, w) = decide_word(guide_words, lines_pdf)

    print("index : " + str(i))
    print("ocurrencias : " + str(max_))
    print("str : " + str(w))
    return (i,max_, w)

def extract_texttract(filein, fileout_txt):
    text = textract.process(filein)

    data = codecs.open(fileout_txt,'wb')
    data.write(text)
    data.close()

    lines_pdf = []
    with codecs.open(fileout_txt,'r') as f:
        lines_pdf = f.readlines()
    
    con_newl = len(lines_pdf)
    #print("con new line : " + str(len(lines_pdf)))
    f.close()

    #numerar las paginas
    nuevo = codecs.open(fileout_txt, 'w')
    n_page = 1
    for line_pdf in lines_pdf:
        if(line_pdf.strip() == '### new line ###'):
            n_page +=1
        else:
            nuevo.write(str(n_page)+'<-->'+line_pdf)
    nuevo.close()

    #print("number of pages : "+ str(n_page))
    lines_pdf = []
    with codecs.open(fileout_txt,'r') as f:
        lines_pdf = f.readlines()

    #print("sin new line : " + str(len(lines_pdf)))
    f.close()
    sin_newl = len(lines_pdf)
    if(n_page == sin_newl): #só existem pages de label "new line" --> testar se consegue extrair com OCR
        print("Usar OCR-tesseract")
        text = textract.process(filein, method='tesseract')
        
        data = codecs.open(fileout_txt,'wb')
        data.write(text)
        data.close()

        lines_pdf = []
        with codecs.open(fileout_txt,'r') as f:
            lines_pdf = f.readlines()
        
        con_newl = len(lines_pdf)
        #print("con new line : " + str(len(lines_pdf)))
        f.close()

        #numerar las paginas
        nuevo = codecs.open(fileout_txt, 'w')
        n_page = 1
        for line_pdf in lines_pdf:
            if(line_pdf.strip() == '## new line ##'):
                n_page +=1
                #print('aqui')
            else:
                #print(line_pdf.strip())
                nuevo.write(str(n_page)+'<-->'+line_pdf)
        nuevo.close()

        #print("number of pages : "+ str(n_page))
        lines_pdf = []
        with codecs.open(fileout_txt,'r') as f:
            lines_pdf = f.readlines()

        #print("sin new line : " + str(len(lines_pdf)))
        f.close()
        sin_newl = len(lines_pdf)
    
    return (con_newl, sin_newl, lines_pdf)
    

def get_indexs_file(filein, fileout_txt, file_indexs):
    noencontro = 0
    
    (con_newl, sin_newl, lines_pdf) = extract_texttract(filein, fileout_txt)
    #print(lines_pdf)
    print("con new lines : " + str(con_newl))
    print("sin new lines : " + str(sin_newl))
    pages_start = []

    ## obtener la keyword que nos guiara para separar los papers
    minim = 3
    (ind, max_, keyword)=get_keyword_pten(lines_pdf, 3)
    if ind > -1:
        #print(keyword)
        for i in range(len(lines_pdf)-1):
            line = lines_pdf[i]
            #line = line.strip()
            partes = line.split('<-->')
            
            number_page = partes[0]
            str_line = partes[1]
            
            key = keyword 
            if ("<-->" in keyword):
                key = keyword[4:]
                #print(key)
            if (key in str_line):
                print("founded at the page : " + number_page)
                pages_start.append(number_page)


        print("the start pages of each paper:")
        print(pages_start)
        print('\n\n')
    else:
        noencontro = 1
        print("No se encontró la palabra guia" + keyword)
        print("Intentar con otra palabra guia")
        print("Por lo pronto retornaremos el pdf completo")
        pages_start.append('1')
        last_page =int(lines_pdf[-1].split('<-->')[0].strip())
        pages_start.append(str(last_page))
        print(last_page)
    starts = codecs.open(file_indexs, 'w')
    starts.write(','.join(pages_start))
    return noencontro 

def get_indexs_folder(path_pdfedit, path_txt, path_indexs, path_noenc):
    noen_p = codecs.open(path_noenc+"noenc.txt", "w")
    lista = os.listdir(path_pdfedit)
    for item in lista:
        print(item)
        noencontro = get_indexs_file(path_pdfedit+item, path_txt+item+'.txt', path_indexs+item+'.txt')
        if noencontro == 1:
            noen_p.write(path_pdfedit+item + '\n')
    noen_p.close()

# Executar por pastas

path_noenc = '../noenc/Boletins/Boletins1/'
pdfedit_folder = '../temp/Boletins/Boletins1/'
folderout_txt = '../texts_edit/Boletins/Boletins1/'
folder_indexs = '../indexs/Boletins/Boletins1/'
get_indexs_folder(pdfedit_folder, folderout_txt, folder_indexs, path_noenc)

path_noenc = '../noenc/Boletins/Boletins2/'
pdfedit_folder = '../temp/Boletins/Boletins2/'
folderout_txt = '../texts_edit/Boletins/Boletins2/'
folder_indexs = '../indexs/Boletins/Boletins2/'
get_indexs_folder(pdfedit_folder, folderout_txt, folder_indexs, path_noenc)

path_noenc = '../noenc/Boletins/Boletins3/'
pdfedit_folder = '../temp/Boletins/Boletins3/'
folderout_txt = '../texts_edit/Boletins/Boletins3/'
folder_indexs = '../indexs/Boletins/Boletins3/'
get_indexs_folder(pdfedit_folder, folderout_txt, folder_indexs, path_noenc)

path_noenc = '../noenc/Boletins/Boletins4/'
pdfedit_folder = '../temp/Boletins/Boletins4/'
folderout_txt = '../texts_edit/Boletins/Boletins4/'
folder_indexs = '../indexs/Boletins/Boletins4/'
get_indexs_folder(pdfedit_folder, folderout_txt, folder_indexs, path_noenc)

