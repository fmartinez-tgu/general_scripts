
library(adegenet)
library(ape)
library(seqinr)
library(matrixcalc)
library(doParallel)
library(foreach)

args = commandArgs(trailingOnly=TRUE)
registerDoParallel(cores=16)

pairsnp <- read.csv(file=args[1], sep = "\t", check.names = FALSE)
rownames(pairsnp) <- colnames(pairsnp)
print("CSV importado")
dist2=upper.triangle(as.matrix(pairsnp))
print("Matriz superior calculada")

print("Guardando distancias 1")
total_distances=NULL
total_distances<-foreach(i=1:dim(dist2)[1], .errorhandling = 'remove') %dopar%
  {
    distsample=NULL
    for (j in i:dim(dist2)[2]){
      if (rownames(dist2)[i]!=colnames(dist2)[j]) distsample=rbind(distsample,c(rownames(dist2)[i],dist2[i,j],colnames(dist2)[j]))
    }
    return(distsample)
  }
distances=NULL
print("Guardando distancias 2")
for(i in 1:length(total_distances))
{
  distances=rbind(distances, unlist(total_distances[[i]]))
}

print("Guardando fichero de distancias")
name <- gsub(".fas","", args[1])

total_ordered=as.data.frame(distances[order(as.numeric(distances[,2])),])
if (dim(total_ordered)[2]==1) {total_ordered=t(total_ordered)}
total_ordered[,2]=as.numeric(as.character(total_ordered[,2]))
index=which(total_ordered[,2]<= as.integer(args[2]))
total_ordered_cutoff=total_ordered[index,]
write.table(total_ordered, file= paste("genetic_distances", name, sep = "_"), row.names = FALSE, quote = FALSE, col.names =c("Strain1", "diff", "Strain2"))
if (dim(total_ordered)[1] > 1) {write.table(total_ordered_cutoff, file= paste("genetic_distances",name,args[2],"snp", sep="_"), row.names = FALSE, quote = FALSE, col.names =c("Strain1", "diff", "Strain2"))} else {write.table(t(total_ordered_cutoff), file= paste("genetic_distances",name,args[2],"snp", sep="_"), row.names = FALSE, quote = FALSE, col.names =c("Strain1", "diff", "Strain2"))}

