import pandas as pd
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import words
import pprint

file = "archive/db_books"
stories  = "archive/stories"
stopwords = "archive/stopwords.txt"
out_txt = "content/"
out_db = "db/"

def leer_datos(filename, sp ='\t'):
    data = pd.read_csv(filename+".csv", sep = sp)
    return np.array(data.iloc[:,:])


def read_stopwords ():
    with open (stopwords,"r") as f_stop:
        data = f_stop.read()
        return data.split('\n')

def strip_word (query, stopwords):
    querywords = query.split()
    resultwords  = [word for word in querywords if word.lower() not in stopwords]
    result = ' '.join(resultwords)
    return result

def lematizar_string (in_str, lemmatizer):
    out_str = [lemmatizer.lemmatize(word) for word in in_str.split(" ")]
    return ' '.join(out_str)

def main():

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

    print (len(data_db.keys()))

    db_for_del = []

    for key in data_db.keys():
        #print (data_db[key]["language"])
        if data_db[key]["language"] != "English":
            db_for_del += [key]

    for key in db_for_del:
        del data_db[key]

    print (len(data_db.keys()))

    # eliminar stop words

    print (len(data_db["51082.txt"]["content"]))

    stop_words_list = read_stopwords ()

    for key in data_db.keys():
        data_db[key]["content"] = strip_word (data_db[key]["content"], stop_words_list)

    print (len(data_db["51082.txt"]["content"]))


    # Lematizacion
    
    lemmatizer = WordNetLemmatizer()  

    for key in data_db.keys():
        data_db[key]["content"] = lematizar_string (data_db[key]["content"],lemmatizer)
    
    print (len(data_db["51082.txt"]["content"]))


    # Volcar archivos en txt

    for key in data_db.keys():
        with open(out_txt+key,"w") as f:
            f.write(data_db[key]["content"].encode('utf-8').decode('ascii', 'ignore')) 

    # crear indice invertido

    dictionary = words.words()

    for key in data_db.keys():
        for word in data_db[key]["content"].split():
            if word in dictionary: 
                with open (out_db+word+".txt", "a+") as f:
                    f.write(key.strip().strip(".txt")+'\n')
            

    """
    cadenaPalabras = 'it was the best of times it was the worst of times '
    cadenaPalabras += 'it was the age of wisdom it was the age of foolishness'

    listaPalabras2 = cadenaPalabras.split()
    listaPalabras3=set(listaPalabras2)
    listaPalabras=list(listaPalabras3)

    frecuenciaPalab = []
    for w in listaPalabras:
        frecuenciaPalab.append(listaPalabras2.count(w))


    print("Pares\n" + str(list(zip(listaPalabras, frecuenciaPalab))))
    """

if __name__ == "__main__":
    main()
    
    #print(len(words.words()))

