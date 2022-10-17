'''Script para colorear cada cluster de transmisión de nuestra filogenia de un color distinto de forma aleatoria
   en la herramienta iTOL'''

import random
import os
import sys

r = lambda: random.randint(0,255)

color = '#%02X%02X%02X' % (r(),r(),r()) # Genera un color en formato hexadecimal de forma aleatoria

cluster_file = sys.argv[1]
output_name = sys.argv[2]

with open("{0}.txt".format(output_name),"w+") as resultado:
    
    resultado.write("DATASET_COLORSTRIP\nSEPARATOR COMMA\nDATASET_LABEL,{0}\nCOLOR_BRANCHES,0\nDATA\n".format(output_name))
    
    with open(cluster_file,"r+") as fichero:
        
        lineas = fichero.readlines()
        
        for i in range(1,len(lineas)):
            color = '#%02X%02X%02X' % (r(),r(),r())
            linea = lineas[i]
            
            cluster, muestras = linea.split("\t")
            
            muestras_lista = muestras.split(",")
            for i in muestras_lista:
                if "\n" in i:
                    i = i[0:-1]
                resultado.write("{0},{1},{2}\n".format(i,color,cluster))
