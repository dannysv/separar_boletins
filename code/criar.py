import os

os.system('mkdir ../data/')
os.system('mkdir ../indexs')
os.system('mkdir ../noenc')
os.system('mkdir ../papers')
os.system('mkdir ../papers_text')
os.system('mkdir ../temp')
os.system('mkdir ../texts_edit')

lista = os.listdir('../')
for item in lista:
    if item in ['data','indexs', 'noenc', 'papers', 'papers_text', 'temp', 'text_edit']:
        print('mkdir ' + os.path.join(os.path.join('../', item), 'Boletins'))
        os.system('mkdir ' + os.path.join(os.path.join('../', item), 'Boletins'))
        os.system('mkdir ' + os.path.join(os.path.join('../', item), 'Boletins/Boletins1'))
        os.system('mkdir ' + os.path.join(os.path.join('../', item), 'Boletins/Boletins2'))
        os.system('mkdir ' + os.path.join(os.path.join('../', item), 'Boletins/Boletins3'))
        os.system('mkdir ' + os.path.join(os.path.join('../', item), 'Boletins/Boletins4'))

