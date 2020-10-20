import numpy as np
import sys
import pprint
import os.path as path
import cross_prod as vect
from pathlib import Path
import operator
import pickle
from tqdm import tqdm

out_txt = "content/"
vector_dir= "db_vector/"
directory = "db/"
base2= "db2/"



def my_ls(ruta = Path.cwd()):
    return [arch.name for arch in Path(ruta).iterdir() if arch.is_file()]


def abrir_datos(name ):
    with open(name, 'rb') as f:
        return pickle.load(f)

def guardar_datos(dic, nombre):
    with open(base2+nombre+".txt", 'wb') as f:
           pickle.dump(dic, f, pickle.HIGHEST_PROTOCOL)

def printh (*text):
    print ("<p>")
    print (*text)
    print ("</p><br>")

def read_file( word ):
    if word == "names":
        with open (word+".txt", "r") as f_stop:
            data = f_stop.read()
            return data.split('\n')
    else:
        with open (directory+word+".txt","r") as f_stop:
            data = f_stop.read()
            return data.split('\n')

def count_max(lista):
    return {i:lista.count(i) for i in lista}

def union(word1, word2):
    return word1 + word2

def intersection(word1, word2):
    intersection = [i for i in word1 if i in word2]
    return intersection

def leer_datos(filename, sp ='\t'):
    data = pd.read_csv(filename+".csv", sep = sp)
    return np.array(data.iloc[:,:])

def operation(operator, word1, word2):
    if operator == "and":
        return intersection(word1, word2)
    if operator == "or":
        return union(word1, word2)
    else:
        print_error("ERROR")

def oper_not(word):
    list_names=read_file("names")
    return list_names

def process(query2):
    query=list(query2)
    #if len(query)%2==0:
    #    printh("ERROR: ingresa la consulta de la forma: palabra operador palabra")
    #else:
    i = 1
    if path.exists(directory+query[0]+".txt"):
        word1=read_file(query[0])
        result1=word1
        #printh(query[0], ":", word1)
    else:
        print_error("ERROR: la palabra <<<" , query[0], ">>> no se encuentra")
        exit(0)
        result1=[]
        word1=[]
    while i <len(query):
        operator=query[i]
        if path.exists(directory+query[i+1]+".txt"):
            word2=read_file(query[i+1])
            #printh("entre al if", query[i+1], ": ", word2)
            result1=operation(operator, word1, word2)
        elif query[i+1] == "not":
            result1=oper_not(query[i+2])
            i=i+1
        else:
            print_error("no entré ERROR: la palabra <<<" , query[i+1], ">>> no se encuentra")
            exit(0)
        word1=result1
        #printh("resultado parcial iteración : ",i, "  resultado: ", word1)
        i=i+2
    #printh("resultado de consulta:", word1)
    return word1

def show_result(recomended_name):
    #print(recomended_name)
    with open (out_txt+recomended_name+".txt") as f:
        first_line = f.readline().split("%")
        content = f.read()
        return (first_line[0].strip(),first_line[1].strip(),content)




def print_text_html (id, title, author, content):
    print ("""<div class="col mb-4">
                        <div class="card border-dark">
                          <div class="card-header">
                                """+id+"""
                          </div>
                          <div class="card-body">
                                <h5 class="card-title">"""+title+"""</h5>
                                <p class="card-text">"""+content+"""</p>
                                <p class="card-text"><small class="text-muted">Autor: """+author+"""</small></p>
                          </div>
                        </div>
                </div>""")

def print_text_html_sec (id, title, author, content):
    print ("""<div class="col mb-4">
                        <div class="card text">
                          <div class="card-header">
                                """+id+"""
                          </div>
                          <div class="card-body">
                                <h5 class="card-title">"""+title+"""</h5>
                                <p class="card-text">"""+content+"""</p>
                                <p class="card-text"><small class="text-muted">Autor: """+author+"""</small></p>
                          </div>
                        </div>
                </div>""")



def print_alert (string_d):
    print ('<div class="alert alert-primary" role="alert">')
    print (string_d)
    print ("</div>")

def print_error (string_d):
    print ('<div class="alert alert-danger" role="alert">')
    print (string_d)
    print ("</div>")

def read_data_simil (name_file, quantity):
    x = abrir_datos(name_file)
    s = [(k, v) for k, v in sorted(x.items(), key=lambda item: item[1], reverse=True)]
    return (s[:quantity])

      
def read_vector( word ):
    with open (vector_dir+word,"r") as f_stop:
        data = f_stop.read()
        return data.split('\n')

def get_recomendations( recomended):
    all_files=my_ls(vector_dir)
    vect_rec=read_vector(recomended)
    dicc_rec = {}
    for i in tqdm(all_files):
        temp=read_vector(i)
        a=list(map(int, vect_rec[:-1]))
        b=list(map(int, temp[:-1]))
        rank=vect.process(a, b)
        dicc_rec[i.split('.')[0]] = rank
    result_sort = dict(sorted(dicc_rec.items(), key=operator.itemgetter(1)))
    guardar_datos(result_sort, recomended)


def read_similes (name, number):
    if not path.isfile(base2+name+".txt.txt"):
        get_recomendations(name+".txt")

    data = read_data_simil(base2+name+".txt.txt",number)
    for tex in data[1:]:
        texto = show_result(tex[0])

        formatted_float = "{:.2f}".format(100*(tex[1]))
        print_text_html_sec(tex[0]+" Porcentaje: "+formatted_float+" %", texto[0],texto[1],texto[2][:200]+" ...")
  


def main():
    #print("consulta: ")
    #query2 = input().split(' ')
    sys.argv.pop(0)
    query=sys.argv
    quantity = int(query[0])
    print_alert("Consulta: "+str(query[1:]))
    if(len(sys.argv)-1 % 2 != 0):
        resultado=process(query[1:])
        result=count_max(resultado)
        recomended=max(result, key=result.get)
        texto = show_result(recomended)

        print('<div class="row row-cols-1 row-cols-md-2">')

        print_text_html(recomended, texto[0],texto[1],texto[2][:200]+" ...")

        read_similes (recomended, quantity)

        print('</div>')

    else:
        print_error("ERROR: ingresa la consulta de la forma palabra and/or palabra")
    


 
if __name__ == "__main__":
    main()
    

