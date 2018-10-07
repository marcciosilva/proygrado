setwd("~/proygrado/normalidad_graficos")
library("plotly")
library("pracma")

add_ranges_to_data = function(data,tareas,description){
  entry = 1
  size = length(names(data))
  for (i in c(200,400,600,800,1000,1200)){
    from = i - 200
    to = i
    values_to_observe = data[,tareas] < to & data[,tareas] >= from
    if (to == 200)
      data[values_to_observe,size + 1] = paste(paste(entry,".",sep=""),"Entre 17 y",to,sep=" ")
    else if (to == 1200)
      data[values_to_observe,size + 1] = paste(paste(entry,".",sep=""),"Entre",from,"y 1024",sep=" ")
    else
      data[values_to_observe,size + 1] = paste(paste(entry,".",sep=""),"Entre",from,"y",to,sep=" ")
    
    entry = entry + 1
  }
  names(data)[size + 1] = "rango"
  data[,size + 2] = description
  names(data)[size + 2] = "Clasificador"
  return(data)
}

create_data_frame <- function(filename){
  classifier = read.csv(paste("csvs/",filename,sep=""))
  size = length(names(classifier))
  classifier[,size + 1] = classifier$esperado - classifier$obtenido
  names(classifier)[size + 1] = "diff_esperado_con_obtenido"
  classifier[,size + 2] = (classifier$obtenido / classifier$esperado * 100) - 100
  names(classifier)[size + 2] = "diff_porcentual"
  return(classifier)
}

get_data = function(file_name,description){
  ann512 = create_data_frame(file_name)
  svm512 = create_data_frame("512x16-svm.csv")
  
  ann512 = add_ranges_to_data(ann512,4,description)
  svm512 = add_ranges_to_data(svm512,4,"SVM")
  all_data = rbind(ann512,svm512)
  return(all_data)  
}

## IDENTITY:
name = "identity_2"
all_data = get_data(paste(name,".csv",sep=""),"ANN - 2 capas ocultas. Activación: identity.")
title = "Comparación entre Red Neuronal y Máquina de Soporte Vectorial."
x_title = "Rango de tareas en dimensiones estudiadas."
y_title = "Porcentaje de diferencia entre makespan obtenido y esperado. \n(obtenido - esperado) x 100"
subtitle = "Porcentaje de diferencia entre makespan obtenido y esperado en clasificación. \SVM y ANN 2 capas ocultas con activación Identity."
Y = all_data$diff_porcentual
p <- ggplot(all_data) + 
  geom_boxplot(outlier.shape= NA, data=all_data,aes(x=all_data$rango, y=Y,fill=Clasificador),position=position_dodge(width = 0.9)) +
  scale_fill_grey(start = 0.4, end = 1) +
  coord_cartesian(ylim=c(100,0)) +
  ggtitle(title) + labs(subtitle=subtitle,x=x_title,y=y_title) +
  theme(plot.title = element_text(family = "Roboto", color="#666666", face="bold", size=11, hjust=0)) +
  theme(axis.title = element_text(family = "Roboto", color="#666666", face="bold", size=9)) +
  theme(plot.subtitle = element_text(family = "Roboto", color="#666666", size=11)) +
  theme(legend.position="bottom")
ggsave("2_medianas_diferenciasann_2_capas_ocultas_identity.png",width = 25, height = 15, units = "cm",dpi = 300)


title = "Comparación entre Red Neuronal y Máquina de Soporte Vectorial."
x_title = "Rango de tareas en dimensiones estudiadas."
y_title = "Precisión en clasificación."
subtitle = "Precisión en clasificación. \nSVM y ANN 2 capas ocultas con activación Identity."
Y = all_data$accuracy
p <- ggplot(all_data) + 
  geom_boxplot(outlier.shape= NA, data=all_data,aes(x=all_data$rango, y=Y,fill=Clasificador),position=position_dodge(width = 0.9)) +
  scale_fill_grey(start = 0.4, end = 1) +
  coord_cartesian(ylim=c(0.75,0.6)) +
  ggtitle(title) + labs(subtitle=subtitle,x=x_title,y=y_title) +
  theme(plot.title = element_text(family = "Roboto", color="#666666", face="bold", size=11, hjust=0)) +
  theme(axis.title = element_text(family = "Roboto", color="#666666", face="bold", size=9)) +
  theme(plot.subtitle = element_text(family = "Roboto", color="#666666", size=11)) +
  theme(legend.position="bottom")
ggsave("3_accuracy_ann_2_capas_ocultas_identity.png",width = 25, height = 15, units = "cm",dpi = 300)


title = "Comparación entre Red Neuronal y Máquina de Soporte Vectorial."
x_title = "Rango de tareas en dimensiones estudiadas."
y_title = "Porecentaje de selecciones de máquinas erroneas en\n las que se selecciona una mejor máquina"
subtitle = "Precisión en clasificación. \nSVM y ANN 2 capas ocultas con activación Identity."
Y = all_data$porcentaje_mejores * 100
p <- ggplot(all_data) + 
  geom_boxplot(outlier.shape= NA, data=all_data,aes(x=all_data$rango, y=Y,fill=Clasificador),position=position_dodge(width = 0.9)) +
  scale_fill_grey(start = 0.4, end = 1) +
  coord_cartesian(ylim=c(0,25)) +
  ggtitle(title) + labs(subtitle=subtitle,x=x_title,y=y_title) +
  theme(plot.title = element_text(family = "Roboto", color="#666666", face="bold", size=11, hjust=0)) +
  theme(axis.title = element_text(family = "Roboto", color="#666666", face="bold", size=9)) +
  theme(plot.subtitle = element_text(family = "Roboto", color="#666666", size=11)) +
  theme(legend.position="bottom")
ggsave("4_porcentaje_maquinas_mejores_ann_2_capas_ocultas_identity.png",width = 25, height = 15, units = "cm",dpi = 300)


title = "Comparación entre Red Neuronal y Máquina de Soporte Vectorial."
x_title = "Rango de tareas en dimensiones estudiadas."
y_title = "Error relativo del makespan agregado por la selección de máquinas erroneas\n(obtenido - esperado)/esperado"
subtitle = "Error relativo. \nSVM y ANN 2 capas ocultas con activación Identity."
Y = all_data$porcentaje_mejores * 100
p <- ggplot(all_data) + 
  geom_boxplot(outlier.shape= NA, data=all_data,aes(x=all_data$rango, y=Y,fill=Clasificador),position=position_dodge(width = 0.9)) +
  scale_fill_grey(start = 0.4, end = 1) +
  coord_cartesian(ylim=c(0,25)) +
  ggtitle(title) + labs(subtitle=subtitle,x=x_title,y=y_title) +
  theme(plot.title = element_text(family = "Roboto", color="#666666", face="bold", size=11, hjust=0)) +
  theme(axis.title = element_text(family = "Roboto", color="#666666", face="bold", size=9)) +
  theme(plot.subtitle = element_text(family = "Roboto", color="#666666", size=11)) +
  theme(legend.position="bottom")
ggsave("6_error_relativo_ann_2_capas_ocultas_identity.png",width = 25, height = 15, units = "cm",dpi = 300)
