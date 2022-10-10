''' Este script colorea cada muestra con el color correspondiente a su linaje en el iTOL. Como input, toma
    la tabla obtenida con las muestras y sus linajes del script de resistencias'''

import os
import sys

output_file = sys.argv[2]
resistance_file = sys.argv[1]


with open(output_file,"w+") as resultado:
    resultado.write("TREE_COLORS\nSEPARATOR TAB\nDATA\n")
    
    with open(resistance_file,"r") as fichero:
        
        lineas = fichero.readlines()
        
        for i in range(1,len(lineas)):
            
            linea = lineas[i]
            col = linea.split("\t")
            err = col[0]
            err_f, res = err.split(".")
            filo = col[14]
                      
            
            if "coinfection" in filo:
                continue
            
            elif "lineage1" in filo:
                resultado.write("{0}\t{1}\t{2}\tnormal\n".format(err_f,"label_background","#fb2afb")) # Color morado
            
            elif "lineage2" in filo:
                resultado.write("{0}\t{1}\t{2}\tnormal\n".format(err_f,"label_background","#0d25f6")) # Color azul
            
            elif "lineage3" in filo:
                resultado.write("{0}\t{1}\t{2}\tnormal\n".format(err_f,"label_background","#7c0e7c")) # Color verde
            
            elif "lineage4" in filo:
                resultado.write("{0}\t{1}\t{2}\tnormal\n".format(err_f,"label_background","#f00d2b")) # Color rojo

            elif "lineage5" in filo:
                resultado.write("{0}\t{1}\t{2}\tnormal\n".format(err_f,"label_background","#810F2F")) # Color marrón
            
            elif "lineage6" in filo:
                resultado.write("{0}\t{1}\t{2}\tnormal\n".format(err_f,"label_background","#427A16")) # Color verde
            
            elif "lineage6" in filo:
                resultado.write("{0}\t{1}\t{2}\tnormal\n".format(err_f,"label_background","#F1BE2B")) # Color verde
            
            elif "Bovis" or "Caprae" or "Animal" in filo:
                resultado.write("{0}\t{1}\t{2}\tnormal\n".format(err_f,"label_background","#FF0004")) # Color amarillo
