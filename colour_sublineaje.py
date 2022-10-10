'''Este script toma un archivo con el formato MUESTRA\tLINAJE_DE_LA_TABLA y anota de manera aleatoria a nivel de sublinaje'''


import os
import sys

file_sub = sys.argv[1]
output_file = sys.argv[2]



import random
r = lambda: random.randint(0,255) # Generador aleatorio de colores para colorear los sublinajes

sublinaje_dic = {}


with open(file_sub,"r+") as fichero:

    lineas = fichero.readlines()

    with open("{0}.txt".format(output_file),"w+") as resultado:

        resultado.write("DATASET_COLORSTRIP\nSEPARATOR COMMA\nDATASET_LABEL,{0}\nCOLOR_BRANCHES,0\nDATA\n".format(output_file))

        for linea in lineas:

            sample, linaje = linea.split("\t")

            sample = sample.rstrip()
            linaje = linaje.rstrip()

            if linaje in sublinaje_dic.keys():

                sublinaje_dic[linaje].append(sample)

            else:
                sublinaje_dic[linaje] = [sample]

        
        for key, values in sublinaje_dic.items():
            
            color = '#%02X%02X%02X' % (r(),r(),r())

            for value in values:

                resultado.write("{0},{1},{2}\n".format(value, color, key))
