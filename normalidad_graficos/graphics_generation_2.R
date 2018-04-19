library("plotly")
library("pracma")
library("ggplot2")
setwd("~/proygrado/normalidad_graficos")

create_data_frame <- function(filename){
  classifier = read.csv(paste("csvs/con_accuracy/",filename,sep=""))
  length(names(classifier))
  classifier[,6] = classifier$esperado - classifier$obtenido
  names(classifier)[6] = "diff_esperado_con_obtenido"
  classifier[,7] = (classifier$obtenido / classifier$esperado * 100) - 100
  names(classifier)[7] = "diff_porcentual"
  return(classifier)
}

get_max_mins_meds_by_range = function(data,tareas,valor_a_analizar){
  entry = 1
  calcs = data.frame(matrix(vector(),0,3))
  
  for (i in c(200,400,600,800,1000,1200)){
    from = i - 200
    to = i
    values_to_observe = data[,tareas] < to & data[,tareas] >= from
    new_data = data[values_to_observe,valor_a_analizar]
    calcs = rbind(calcs, data.frame(A="Máximo",B=max(new_data),C=paste(from,to,sep=":")))
    calcs = rbind(calcs, data.frame(A="Mediana",B=median(new_data),C=paste(from,to,sep=":")))
    calcs = rbind(calcs, data.frame(A="Mínimo",B=min(new_data),C=paste(from,to,sep=":")))
  }
  names(calcs) = c("key","vale","range")
  return(calcs)
}

# esta gráfica es para generar en barra
plot_bar_chart_with_medians = function(data,title,subtitle,x_title,y_title){
  p <- ggplot(data=data, aes(x=range, y=vale, fill=key)) +
    geom_bar(stat="identity", position=position_dodge()) +
    geom_text(aes(label=round(vale,digits=2)),position=position_dodge(width=0.9), vjust=-0.2, size=3.5) +
    scale_fill_grey(start = 0, end = 1) +
    ggtitle(title) + labs(subtitle=subtitle,x=x_title,y=y_title) +
    theme(plot.title = element_text(family = "Roboto", color="#666666", face="bold", size=11, hjust=0)) +
    theme(axis.title = element_text(family = "Roboto", color="#666666", face="bold", size=9)) +
    theme(plot.subtitle = element_text(family = "Roboto", color="#666666", size=11))  
  return(p)
}

# type must be "accuracy" or "percentage" or "abs_diff"
plot_point_char_for_medians = function(data,title,subtitle,x_title,y_title,type){
  if (type == "accuracy"){
    medians = get_max_mins_meds_by_range(data,4,3)  
  }else if(type == "percentage"){
    medians = get_max_mins_meds_by_range(data,4,7)
  }else if(type == "abs_diff"){
    medians = get_max_mins_meds_by_range(data,4,6)
    medians$vale = abs(medians$vale)
  }
  
  max_to_observe = medians[medians$key == "Máximo",]
  med_to_observe = medians[medians$key == "Mediana",]
  min_to_observe = medians[medians$key == "Mínimo",]
  
  p <- ggplot(data=max_to_observe,aes(x=max_to_observe$range)) +
    geom_point(aes(y=med_to_observe$vale),shape=19, size=3) + geom_text(aes(y=med_to_observe$vale, label=round(med_to_observe$vale,digits=2)),hjust=0.5, vjust=-0.6) +
    geom_point(aes(y=min_to_observe$vale),shape=19, size=2, color="gray40") + geom_text(aes(y=min_to_observe$vale, label=round(min_to_observe$vale,digits=2)),hjust=0.5, vjust=-0.6) +
    geom_point(aes(y=max_to_observe$vale),shape=19, size=2, color="gray40") + geom_text(aes(y=max_to_observe$vale, label=round(max_to_observe$vale,digits=2)),hjust=0.5, vjust=-0.6) +
    ggtitle(title) + labs(subtitle=subtitle,x=x_title,y=y_title) +
    theme(plot.title = element_text(family = "Roboto", color="#666666", face="bold", size=11, hjust=0)) +
    theme(axis.title = element_text(family = "Roboto", color="#666666", face="bold", size=9)) +
    theme(plot.subtitle = element_text(family = "Roboto", color="#666666", size=11))  
  return(p)
  
}



plot_medians_for_percentage = function(data,title,subtitle,x_title,y_title){
  medians = get_max_mins_meds_by_range(data,4,7)
  #medians_plot = plot_bar_chart_with_medians(medians,title,subtitle,x_title,y_title)
  return(medians_plot)
}

plot_medians_for_accuracy = function(data,title,subtitle,x_title,y_title){
  medians = get_max_mins_meds_by_range(data,4,3)
  #medians_plot = plot_bar_chart_with_medians(medians,title,subtitle,x_title,y_title)
  return(medians_plot)
}
## ANN128x4
ann128 = create_data_frame("128x4-ann.csv")
title = "Máximos, medianas y mínimos\nen diferencias porcentuales de makespan"
subtitle = "ANN entrenada con instancias de dimensión 128x4"
x_title = "Rangos de tareas"
y_title = "Differencia en makespan (%)"
percentage_medians_plot = plot_point_char_for_medians(ann128,title,subtitle,x_title,y_title,"percentage")

title = "Máximos, medianas y mínimos\nen diferencias de accuracy en clasificación"
subtitle = "ANN entrenada con instancias de dimensión 128x4"
x_title = "Rangos de tareas"
y_title = "Accuracy"
accuracy_medians_plot = plot_point_char_for_medians(ann128,title,subtitle,x_title,y_title,"accuracy")

title = "Máximos, medianas y mínimos\nen diferencias absolutas entre makespan obtenido y esperado"
subtitle = "ANN entrenada con instancias de dimensión 128x4"
x_title = "Rangos de tareas"
y_title = "Diferencia de makespan absoluto"
absolute_differences_plot = plot_point_char_for_medians(ann128,title,subtitle,x_title,y_title,"abs_diff")

## SVM128x4
svm128 = create_data_frame("128x4-svm.csv")
title = "Máximos, medianas y mínimos\nen diferencias porcentuales de makespan"
subtitle = "SVM entrenada con instancias de dimensión 128x4"
x_title = "Rangos de tareas"
y_title = "Differencia en makespan (%)"
percentage_medians_plot = plot_point_char_for_medians(svm128,title,subtitle,x_title,y_title,"percentage")

title = "Máximos, medianas y mínimos\nen diferencias de accuracy en clasificación"
subtitle = "SVM entrenada con instancias de dimensión 128x4"
x_title = "Rangos de tareas"
y_title = "Accuracy"
accuracy_medians_plot = plot_point_char_for_medians(svm128,title,subtitle,x_title,y_title,"accuracy")

title = "Máximos, medianas y mínimos\nen diferencias absolutas entre makespan obtenido y esperado"
subtitle = "SVM entrenada con instancias de dimensión 128x4"
x_title = "Rangos de tareas"
y_title = "Diferencia de makespan absoluto"
absolute_differences_plot = plot_point_char_for_medians(svm128,title,subtitle,x_title,y_title,"abs_diff")

## 512x16 ANN
ann512 = create_data_frame("512x16-ann.csv")
title = "Máximos, medianas y mínimos\nen diferencias porcentuales de makespan"
subtitle = "ANN con dos capas ocultas\nentrenada con instancias de dimensión 512x16"
x_title = "Rangos de tareas"
y_title = "Differencia en makespan (%)"
percentage_medians_plot = plot_point_char_for_medians(ann512,title,subtitle,x_title,y_title,"percentage")

title = "Máximos, medianas y mínimos\nen diferencias de accuracy en clasificación"
subtitle = "ANN con dos capas ocultas\nentrenada con instancias de dimensión 512x16"
x_title = "Rangos de tareas"
y_title = "Accuracy"
accuracy_medians_plot = plot_point_char_for_medians(ann512,title,subtitle,x_title,y_title,"accuracy")

title = "Máximos, medianas y mínimos\nen diferencias absolutas entre makespan obtenido y esperado"
subtitle = "ANN con dos capas ocultas\nentrenada con instancias de dimensión 512x16"
x_title = "Rangos de tareas"
y_title = "Diferencia de makespan absoluto"
absolute_differences_plot = plot_point_char_for_medians(ann512,title,subtitle,x_title,y_title,"abs_diff")

#ANN 512x16 3 capas ocultas
ann512_3capas = create_data_frame("512x16-ann-3capas.csv")
title = "Máximos, medianas y mínimos\nen diferencias de accuracy en clasificación"
subtitle = "ANN con tres capas ocultas\nentrenada con instancias de dimensión 512x16"
x_title = "Rangos de tareas"
y_title = "Accuracy"
accuracy_medians_plot = plot_point_char_for_medians(ann512_3capas,title,subtitle,x_title,y_title,"accuracy")

#ANN 512x16 3 capas ocultas
ann512_4capas = create_data_frame("512x16-ann-4capas.csv")
title = "Máximos, medianas y mínimos\nen diferencias de accuracy en clasificación"
subtitle = "ANN con cuatro capas ocultas\nentrenada con instancias de dimensión 512x16"
x_title = "Rangos de tareas"
y_title = "Accuracy"
accuracy_medians_plot = plot_point_char_for_medians(ann512_4capas,title,subtitle,x_title,y_title,"accuracy")













