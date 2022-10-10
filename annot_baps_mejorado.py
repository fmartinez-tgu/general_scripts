'''Script para anotar los BAPS al nivel de interés. Llamar como python annot_baps.py <archivo de baps> <nivel de interes> <nombre del output>'''


import os
import sys

file_BAPS = sys.argv[1]
level_of_interest = int(sys.argv[2])
output_file = sys.argv[3]


import random
r = lambda: random.randint(0,255) # Generador aleatorio de colores para colorear los BAPS

baps_dic = {}


with open(file_BAPS,"r+") as fichero:

    with open("{0}.txt".format(output_file),"w+") as resultado:

        resultado.write("DATASET_COLORSTRIP\nSEPARATOR COMMA\nDATASET_LABEL,{0}\nCOLOR_BRANCHES,0\nDATA\n".format(output_file))

        lineas = fichero.readlines()
        
        for i in range(1,len(lineas)): # Para cada línea del archivo, es decir, para cada muestra
            
            linea = lineas[i]

            BAPS_levels = len(linea.split(",")) - 1 # Calculamos el número de niveles BAPS que tiene el archivo

            tokens = linea.split(",") # Dividimos la línea

            ident = tokens[0] # Nos quedamos con el nombre de la muestra y quitamos el "\n" final, por si lo hubiera
            ident = ident.rstrip()

            baps_value = tokens[level_of_interest] # Nos quedamos con el valor del nivel de interés para esa muestra, y le quitamos el "\n" por si lo hubiera
            baps_value = baps_value.rstrip()

            

            if baps_value in baps_dic.keys(): # cambiar "level3" por el nivel que desees anotar
                baps_dic[baps_value].append(ident) # cambiar "level3" por el nivel que desees anotar

            else:
                baps_dic[baps_value] = [ident] # cambiar "level3" por el nivel que desees anotar

        print(baps_dic)

        for i in baps_dic.keys():
            color = '#%02X%02X%02X' % (r(),r(),r())
            for j in baps_dic[i]:
                j = j.rstrip()
                resultado.write("{0},{1},{2}\n".format(j,color,i))
