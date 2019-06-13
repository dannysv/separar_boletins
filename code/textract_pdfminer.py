import os
def main(fullpath_file, only_name, fulloutput_file):
    command = "textract -m pdfminer "+ fullpath_file + " -o " + fulloutput_file +'.txt'
    #command = 'tikapp --jar tika-app-1.20.jar -f '+fullpath_file +' -t'
    print(command)
    os.system(command)

def get_texts(path_pdfs, path_texts):
    lista = os.listdir(path_pdfs)
    for item in lista:
        #print(item.replace)
        item = item.replace(' ', '\ ')
        text = main(path_pdfs+'/'+item, item, path_texts+'/'+ item)


#list the all files in 
path = '../papers/Boletins/Boletins1'
path_to = '../papers_text/Boletins/Boletins1'
get_texts(path, path_to)

#list the all files in 
path = '../papers/Boletins/Boletins2'
path_to = '../papers_text/Boletins/Boletins2'
get_texts(path, path_to)

#list the all files in 
path = '../papers/Boletins/Boletins3'
path_to = '../papers_text/Boletins/Boletins3'
get_texts(path, path_to)

#list the all files in 
path = '../papers/Boletins/Boletins4'
path_to = '../papers_text/Boletins/Boletins4'
get_texts(path, path_to)
