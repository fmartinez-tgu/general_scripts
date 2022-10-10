'''python 1_per_cluster_country_aware.py metadata_datasets <archivo_clusters> <lista_muestras_multifasta>'''

'''Este script toma los metadatos de las muestras de los datasets, un archivo de clusters (sin -senyorito-irving), y la lista de muestras del multifasta, y devuelve una nueva lista
    de muestras compuesta de todas las muestras que NO están en cluster, y 1 muestra de cada cluster calculado. Si en el mismo cluster hay muestras de 2 orígenes, mantiene una de cada'''

import sys
import random



metadata = sys.argv[1]
clusters_file = sys.argv[2]
multifasta_file_samples = sys.argv[3]

# Creamos una lista con las muestras del multifasta del cual nos queremos quedar solo 1 por cluster (además del resto de muestras que NO están en cluster)

multifasta_samples = []

with open(multifasta_file_samples, "r+") as input_multifasta:

    lines = input_multifasta.readlines()

    for i in lines:

        multifasta_samples.append(i.rstrip())
    
# Hasta aquí, correcto


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

one_sample_per_cluster = [] # Lista que contendrá una muestra de cada cluster, o más de una si hay de distintos países
all_samples_in_cluster = [] # Lista que contendrá todas las muestras que hay en cluster


with open(clusters_file, "r+") as input_clusters:

    lines = input_clusters.readlines()

    for i in range(1,len(lines)): # Para cada línea del archivo, es decir, para cada cluster

        line = lines[i]
        cluster, samples = line.split("\t")
        samples = samples.split(",") # Me quedo con las muestras del cluster

        dic_samples = {}    # Genero un diccionario que tenga como clave el país o países de origen de las muestras del cluster, y como valores las muestras de dicho país

        if "Cosc" in (" ").join(samples):

            one_sample_per_cluster.append(random.choice(samples))

            for j in samples:   # Para cada muestra del cluster
            
                j = j.rstrip()
                all_samples_in_cluster.append(j)

            continue
                

        for j in samples:   # Para cada muestra del cluster
            
            j = j.rstrip()

            all_samples_in_cluster.append(j) # Añado la muestra a la lista de todas las muestras en cluster

            for key, values in metadata_dic.items(): # Compruebo a qué país pertenece la muestra, y la añado a la clave correspondiente del diccionario

                if j in values:

                    if key not in dic_samples.keys(): # Si el país no existe como clave, crea una lista y añádela
                        dic_samples[key] = []
                        dic_samples[key].append(j)

                    else:                             # Si el país ya está en el diccionario, añade la muestra
                        dic_samples[key].append(j)

                    break

        # En este punto tenemos un diccionario que contiene todas las muestras del cluster adjudicadas a su país de origen
        
        if len(set(dic_samples.keys())) == 1: # Si hay 1 país de origen, cojo cualquiera de las muestras y la añado a mi lista de muestras del cluster

            one_sample_per_cluster.append(random.choice(list(dic_samples.values())[0]))

        else:                                 # Si hay más de 1 país de origen, cojo una muestra de cada país y la añado a la lista
            
            for key, values in dic_samples.items(): # Para cada par clave-valor, es decir, país-muestras, me quedo con una muestra de cada país

                one_sample_per_cluster.append(random.choice(values))

# Ahora faltaría crear la lista final de muestras que contenga las muestras que NO están en cluster, y de las que sí lo están, 1 por país

final_list = []

for i in multifasta_samples: # Para la lista de muestras en el multifasta

    if i not in all_samples_in_cluster: # Si la muestra NO está en la lista de muestras en cluster, la añado a la lista final

        final_list.append(i)

for i in one_sample_per_cluster:    # Ahora añado a la lista final aquellas muestras representativas de los cluster

    final_list.append(i)

# Ahora guardamos la lista en .txt 

with open("list_of_samples_1_per_cluster.txt", "w+") as output:

    for i in final_list:

        output.write("{0}\n".format(i.rstrip()))
