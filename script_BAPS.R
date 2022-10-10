########################

# Este script calcula los BAPS usando el paquete fastBAPS

########################

rm(list = ls())
#Libraries
library(fastbaps)
library(ape)

args = commandArgs(trailingOnly=TRUE)
#Loading data OK

sparse.data <- import_fasta_sparse_nt(args[1]) # Pasamos el archivo multifasta como argumento
print("MULTIFASTA CARGADO")


sparse.data <- optimise_prior(sparse.data, type = "baps") 

# best_baps_partition: function to combine smaller clusters from a fast hierarchical algorithm to maximise 
# the BAPS likelihood (se le puede meter el baps.hc)

#Function to perform bootstrap replicated of fastbaps
#boot.result <- boot_fast_baps(sparse.data, n.cores = 2)

# Obtención de BAPS a partir de la filogenia


filogenia <- ape::read.tree(args[2])
print("FILOGENIA CARGADA")

ESP_baps <- multi_level_best_baps_partition(sparse.data,filogenia, n.cores = 16, levels = 20)
write.csv(x = ESP_baps, file ="BAPS_output")

print("BAPS CALCULADOS")

#ESP_baps contiene la tabla con los BAPS calculados a distintos niveles
