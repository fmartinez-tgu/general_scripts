#!/bin/bash

cp /home/fmartinez/SCRIPTS/1_por_cluster_not_country_aware.py .

grep '>' ../multifasta/multifasta_snpsites.fas | cut -f 2 -d '>' > samples

cp ../clusters/*_clusters_10snps .

python 1_por_cluster_not_country_aware.py samples *_clusters_10snps

/data/ThePipeline_programs/seqtk/seqtk subseq ../multifasta/multifasta_snpsites.fas list_1_per_cluster.txt > multifasta_sin_clusters.fas
