'''python 1_per_cluster_country_aware.py metadata_datasets <archivo_clusters> <lista_muestras_multifasta>'''

'''Este script toma los metadatos de las muestras de los datasets, un archivo de clusters (sin -senyorito-irving), y la lista de muestras del multifasta, y devuelve un archivo de texto
    con aquellos clusters formados por muestras de distintos países'''

import sys
import random
import subprocess
import os
import glob
from io import StringIO


metadata = sys.argv[1]
clusters_file = sys.argv[2]


# Creamos un diccionario que contiene, para cada país, las sample y run accessions procedentes
# de dicho país

metadata_dic = {}

with open(metadata, "r+") as input_metadata:

    lines = input_metadata.readlines()

    for i in range(1,len(lines)):

        linea = lines[i]

        project, sample, run, collection_date, location, country = linea.split("\t")
        country = country.rstrip()
        sample = sample.rstrip()
        run = run.rstrip()

        if country not in metadata_dic.keys():

            metadata_dic[country] = []
            metadata_dic[country].append(sample)
            metadata_dic[country].append(run)

        else:
            metadata_dic[country].append(sample)
            metadata_dic[country].append(run)

# Abrimos el fichero de cluster que genera el script script-get-clusters.py. 
# Para cada cluster, cogemos todas las muestras y vemos a qué país pertenece.
# Si todas las muestras son del mismo país, se mantiene cualquiera de manera aleatoria.
# Si hay muestras de distintos países, se mantiene 1 de cada


with open(clusters_file, "r+") as input_clusters:

    lines = input_clusters.readlines()

    for i in range(1,len(lines)): # Para cada línea del archivo, es decir, para cada cluster

        line = lines[i]
        cluster, samples = line.split("\t")
        samples = samples.split(",") # Me quedo con las muestras del cluster

        dic_samples = {}    # Genero un diccionario que tenga como clave el país o países de origen de las muestras del cluster, y como valores las muestras de dicho país

        if "Cosc" in (" ").join(samples): # Si el cluster es de muestras de Mireia, lo omitimos

            continue
                
        for j in samples:   # Para cada muestra del cluster
            
            j = j.rstrip()

            for key, values in metadata_dic.items(): # Compruebo a qué país pertenece la muestra, y la añado a la clave correspondiente del diccionario

                if j in values:

                    if key not in dic_samples.keys(): # Si el país no existe como clave, crea una lista y añádela
                        dic_samples[key] = []
                        dic_samples[key].append(j)

                    else:                             # Si el país ya está en el diccionario, añade la muestra
                        dic_samples[key].append(j)

                    break

        # En este punto tenemos un diccionario que contiene todas las muestras del cluster adjudicadas a su país de origen

        if len(set(dic_samples.keys())) > 1: # Si hay más de 1 país de origen

            file_name = cluster + "_mixto"

            with open(file_name, "w+") as output:

                for key, values in dic_samples.items():

                    for value in values:
                        
                        value = value.rstrip()

                        grep_sample = os.popen("grep {0}$'\t' ../metadata_datasets".format(value)).read()

                        #print(grep_sample)
                        output.write("{0}\t{1}\n".format(key, value))

# Ahora vamos a hacer una tabla resumen de los clusters mixtos


archivos_clusters = glob.glob("*")

with open("summary_mixed_clusters.tsv", "w+") as output:

    output.write("Cluster_name\tTotal_samples\tCount_per_country\n")

    for archivo in archivos_clusters: 
        
        # Contamos el total por cluster

        lista = os.popen("cut -f 1 {0} | sort | uniq -c | sed 's/      //g' | sed 's/     //g' | sed 's/    //g'".format(archivo)).read() # Para calcular el % por muestra

        total_muestras_count = 0
        lista = lista.split("\n")


        for fila in lista:

            if fila == '':
                continue

            total_muestras_count = total_muestras_count + int(fila.split(" ")[0])


        for fila in lista:

            numero = int(fila.split(" ")[0])
            pais = (" ").join(fila.split(" ")[1:])

            perc = round((numero/total_muestras_count)*100, 2)

            output.write("{0}\t{1}\t{2} {3} ({4}%)\n".format(archivo, total_muestras_count, numero, pais, perc))
            break
        
        for i in range(1,len(lista)):

            fila = lista[i]

            if fila == '':
                continue

            numero = int(fila.split(" ")[0])
            pais = (" ").join(fila.split(" ")[1:])

            perc = round((numero/total_muestras_count)*100, 2)

            output.write("\t\t{0} {1} ({2}%)\n".format(numero, pais, perc))
