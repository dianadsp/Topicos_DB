import pandas as pd
import numpy as np
import sys
import pprint
import os.path as path
import cross_prod as vect
from pathlib import Path
import operator
import pickle
import threading
from joblib import Parallel, delayed
#from numba import jit, prange
import multiprocessing



out_txt = "content/"    
directory = "db/"
vector_dir= "db_vector/"
base2= "db2/"
counter= 1


def my_ls(ruta = Path.cwd()):
    return [arch.name for arch in Path(ruta).iterdir() if arch.is_file()]


def abrir_datos(name ):
    with open(name, 'rb') as f:
        return pickle.load(f)

def guardar_datos(dic, nombre):
    with open(base2+nombre, 'wb') as f:
           pickle.dump(dic, f, pickle.HIGHEST_PROTOCOL)

def read_file( word ):
    if word=="names":
        with open (word+".txt","r") as f_stop:
            data = f_stop.read()
            return data.split('\n')
    else:
        with open (directory+word+".txt","r") as f_stop:
            data = f_stop.read()
            return data.split('\n')

def read_vector( word ):
    with open (vector_dir+word,"r") as f_stop:
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
        print("ERROR")

def oper_not(word):
    list_names=read_file("names")
    return list_names

def process(query2):
    query=list(query2)
#    if len(query)%2==0:
#        print("ERROR: ingresa la consulta de la forma: palabra operador palabra")
#    else:
    i = 2
    if path.exists(directory+query[1]+".txt"):
        word1=read_file(query[1])
        result1=word1
        print(query[1], ":", word1)
    else:
        print("ERROR: la palabra <<<" , query[i+1], ">>> no se encuentra")
        exit(0)
        result1=[]
        word1=[]
    while i <len(query):
        operator=query[i]
        if path.exists(directory+query[i+1]+".txt"):
            word2=read_file(query[i+1])
            print(query[i+1], ": ", word2)
            result1=operation(operator, word1, word2)
        elif query[i+1] == "not":
            result1=oper_not(query[i+2])
            i=i+1
        else:
            print("ERROR: la palabra <<<" , query[i+1], ">>> no se encuentra")
            exit(0)
        word1=result1
        print("resultado parcial iteracion : ",i, "  resultado: ", word1)
        i=i+2
    return word1

def show_result(recomended_name):
    print(recomended_name)
    with open (out_txt+recomended_name+".txt") as f:
        first_line = f.readline().split("%")
        content = f.read()
        return (first_line[0].strip(),first_line[1].strip(),content)
        
    data_db = {}
    data_db_books=leer_datos(file,',')
    #print(data_db_books)
    #print(data_db_books.shape)
    stories_=leer_datos(stories,',')
    #print(stories_.shape)
    #print(stories_[0][0])
    for i in data_db_books:
        data_db[i[0]]={"title":i[1],"author":i[2],"language":i[3].strip()}
    for i in stories_:
        data_db[i[0]]["content"] = i[1]
    # eliminar otros idiomas
    #print (len(data_db.keys()))
    db_for_del = []
    for key in data_db.keys():
        #print (data_db[key]["language"])
        if data_db[key]["language"] != "English":
            db_for_del += [key]
    for key in db_for_del:
        del data_db[key]
    print (data_db[recomended_name+".txt"]["content"])



def get_recomendations( recomended):
    all_files=my_ls(vector_dir)
    print(".")
    #results = [0] * number_rec
    #vect_rec=read_vector(recomended+".txt")
    vect_rec=read_vector(recomended)
    dicc_rec = {}
    for i in all_files:
        temp=read_vector(i)
        a=list(map(int, vect_rec[:-1]))
        b=list(map(int, temp[:-1]))
        rank=vect.process(a, b)
        dicc_rec[i.split('.')[0]] = rank
    result_sort = dict(sorted(dicc_rec.items(), key=operator.itemgetter(1)))
    guardar_datos(result_sort, recomended)
    #result_sort = sorted(dicc_rec.items(), key=operator.itemgetter(1), reverse=True)
    #for name in enumerate(result_sort):
    #    print(name[1][0], 'has spend', dicc_rec[name[1][0]])
    
        



def main():
    count=1
    #sys.argv.pop(0)
    #query=sys.argv
    #number_rec=int(query[0])
    #print("la consulta: ", query)
    vec_files=my_ls(vector_dir)
    ok_file=[]

    for w in my_ls(base2):
        ok_file += [w[:-4]]

    print (len(vec_files))
    print (len(ok_file))

    all_files = list(set(vec_files)-set(ok_file))
    print (len(all_files))

    #if(len(sys.argv)-1 % 2 != 0):
    #    resultado=process(query)
    #    result=count_max(resultado)
    #    recomended=max(result, key=result.get)
    #    print("Documento recomendado: ")
    #    texto = show_result(recomended)
    #    print("Titulo:", texto[0])
    #    print("Autor:", texto[1])
        #print("Contenido:", texto[2])
    #else:
    #    print("ERROR: ingresa la consulta de la forma palabra and/or palabra")
    
##    for i in all_files:
##        get_recomendations( i.split('.')[0])
##        print(count)
##        count=count+1
    #get_recomendations(number_rec, recomended)   
    pool = multiprocessing.Pool(processes=8)
    # if number of processes is not specified, it uses the number of core
    F[:] = pool.map(get_recomendations, all_files ) 
  

def read_data_simil (name_file, quantity):
    x = abrir_datos(name_file)
    s = [(k, v) for k, v in sorted(x.items(), key=lambda item: item[1], reverse=True)]
    return (s[:quantity])


 
if __name__ == "__main__":
    #pprint.pprint (read_data_simil ("163.txt.txt",10))
    main()
    

