'''Script para dejar 1 muestra por cluster, pero sin revisar el origen de las muestras. Este script se usará con los pop. based datasets ya que todas las muestras son del mismo país'''

import sys
import random

multifasta_list = sys.argv[1]
clusters_file_samples = sys.argv[2]


# Creamos una lista donde añadimos todas las muestras del multifasta
multifasta_samples = []

with open(multifasta_list, "r+") as multifasta:

    lineas = multifasta.readlines()

    for linea in lineas:

        multifasta_samples.append(linea.rstrip())


# Ahora, creamos una nueva lista que incluya TODAS las muestras en cluster, y una 2a lista que contenga una muestra aleatoria por cada cluster

muestras_en_cluster = []
muestra_unica_por_cluster = []

with open(clusters_file_samples, "r+") as clusters_file:

    lineas = clusters_file.readlines()

    lineas = lineas[1:]

    for linea in lineas:

        cluster, samples = linea.split("\t")

        samples_list = samples.split(",")

        muestra_unica_por_cluster.append(random.choice(samples_list).rstrip())

        for i in samples_list:

            muestras_en_cluster.append(i.rstrip())

print("MUESTRAS EN CLUSTER:", muestras_en_cluster)
print("UNA POR CLUSTER", muestra_unica_por_cluster)

with open("list_1_per_cluster.txt", "w+") as output:

    for i in multifasta_samples:

        if i not in muestras_en_cluster:
            
            output.write("{0}\n".format(i))

    
    for i in muestra_unica_por_cluster:

        output.write("{0}\n".format(i))
