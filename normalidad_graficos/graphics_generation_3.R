setwd("~/proygrado/normalidad_graficos")
library("plotly")
library("pracma")

create_data_frame <- function(filename){
  classifier = read.csv(paste("csvs/con_accuracy/",filename,sep=""))
  length(names(classifier))
  classifier[,6] = classifier$esperado - classifier$obtenido
  names(classifier)[6] = "diff_esperado_con_obtenido"
  classifier[,7] = (classifier$obtenido / classifier$esperado * 100) - 100
  names(classifier)[7] = "diff_porcentual"
  return(classifier)
}

create_polynomial_fit = function(degree,x,y){
  params = polyfit(x,y,degree)
  fited_y_for_data = 0
  index = 1
  for (i in degree:0){
    fited_y_for_data = fited_y_for_data  + params[index] * x^i
    index = index + 1
  }
  #fited_y_for_data1 = parameters_data1[1]*(data1$tareas)^3 + parameters_data1[2]*(data1$tareas)^2 + (parameters_data1[3])  
  return(fited_y_for_data)
}

create_electrocardiogram = function(data1,data2,name_data1,name_data2,train_dimension){
  fited_y_for_data1 = create_polynomial_fit(3,data1$tareas,data1$diff_porcentual)
  fited_y_for_data2 = create_polynomial_fit(3,data2$tareas,data2$diff_porcentual)
  p <- plot_ly(data1, x = ~tareas, y = ~diff_porcentual, name = name_data1, type = 'scatter', mode="line",opacity=0.5,line = list(color = 'blue', width = 0.5)) %>%
    add_trace(y = fited_y_for_data1, mode = 'lines',line = list(color = 'blue', width = 2),showlegend = FALSE) %>%
    add_trace(y = data2$diff_porcentual, name = name_data2, mode = 'lines',opacity=0.5,line = list(color = 'red', width = 0.5)) %>%
    add_trace(y = fited_y_for_data2, mode = 'lines',line = list(color = 'red', width = 2),showlegend = FALSE) %>%
    layout(title = paste("Escalado en tareas.",train_dimension),
           legend = list(x = 0.5, y = 0.9),
           xaxis = list(title = "número de tareas"),
           yaxis = list (title = "diferencia al makespan esperado (%)"))
  return(p)
}


add_ranges_to_data = function(data,tareas,description){
  entry = 1
  for (i in c(200,400,600,800,1000,1200)){
    from = i - 200
    to = i
    values_to_observe = data[,tareas] < to & data[,tareas] >= from
    data[values_to_observe,8] = paste(entry,"-",from,":",to,sep="")
    entry = entry + 1
  }
  names(data)[8] = "rango"
  data[,9] = description
  names(data)[9] = "Clasificador"
  return(data)
}

create_box_plot = function(all_data,title,x_title,y_title,subtitle,Y){
  p <- ggplot(all_data) + 
    geom_boxplot(data=all_data,aes(x=all_data$rango, y=Y,fill=Clasificador),position=position_dodge(width = 0.9)) +
    scale_fill_grey(start = 0.4, end = 1) +
    ggtitle(title) + labs(subtitle=subtitle,x=x_title,y=y_title) +
    theme(plot.title = element_text(family = "Roboto", color="#666666", face="bold", size=11, hjust=0)) +
    theme(axis.title = element_text(family = "Roboto", color="#666666", face="bold", size=9)) +
    theme(plot.subtitle = element_text(family = "Roboto", color="#666666", size=11)) +
    theme(legend.position="bottom")
  return(p)
}
create_graphics = function(file_name,dimension,description,file_post_fix){
  #ELECTRO:
  Sys.setenv("plotly_username"="mauro.pico")
  Sys.setenv("plotly_api_key"="WOKV1PDMqCVFMP7XqW22")
  ann512 = create_data_frame(file_name)
  svm512 = create_data_frame("512x16-svm.csv")
  comparacion_ann_svm = create_electrocardiogram(ann512,svm512,description,"svm",dimension)
  plotly_IMAGE(comparacion_ann_svm,out_file = paste("1_escalado_tareas_",file_post_fix,".png"))
  
  
  ann512 = add_ranges_to_data(ann512,4,description)
  svm512 = add_ranges_to_data(svm512,4,"SVM")
  all_data = rbind(ann512,svm512)
  
  box_plot_percentage = create_box_plot(all_data,
                                        "Máximos, medianas y mínimos en clasificación de taras por rango",
                                        "Rango de tareas",
                                        "Diferencia entre makespan obtenido y esperado (%)",
                                        paste("Diferencia entre makespan obtenido y esperado en clasificación\nSVM y",description,"Dimension:",dimension),
                                        all_data$diff_porcentual
                                        )
  ggsave(paste("2_medianas_diferencias",file_post_fix,".png",sep=""),width = 25, height = 15, units = "cm",dpi = 300)
  
  box_plot_accuracy = create_box_plot(all_data,
                                        "Máximos, medianas y mínimos en clasificación de taras por rango",
                                        "Rango de tareas",
                                        "Accuracy",
                                        paste("Accuracy para SVM y ",description,"Dimension:",dimension),
                                        all_data$accuracy
  )
  ggsave(paste("3_accuracy_",file_post_fix,".png",sep=""),width = 25, height = 15, units = "cm",dpi = 300)
}

create_graphics("tanh_4.csv","512x16","ANN - 4 capas ocultas. Activación: tanh.","ann_4_capas_ocultas_tanh")

create_graphics("tanh_2.csv","512x16","ANN - 2 capas ocultas. Activación: tanh.","ann_2_capas_ocultas_tanh")

create_graphics("tanh_3.csv","512x16","ANN - 3 capas ocultas. Activación: tanh.","ann_3_capas_ocultas_tanh")

create_graphics("identity_2.csv","512x16","ANN - 2 capas ocultas. Activación: identity.","ann_2_capas_ocultas_identity")

create_graphics("identity_3.csv","512x16","ANN - 3 capas ocultas. Activación: identity.","ann_3_capas_ocultas_identity")

create_graphics("identity_4.csv","512x16","ANN - 4 capas ocultas. Activación: identity.","ann_4_capas_ocultas_identity")

## ACTIVACION TANH:
ann_tanh_2 = create_data_frame("tanh_2.csv")
ann_tanh_2 = add_ranges_to_data(ann_tanh_2,4,"ANN - 2 capas ocultas. Activación: tanh")
ann_tanh_3 = create_data_frame("tanh_3.csv")
ann_tanh_3 = add_ranges_to_data(ann_tanh_3,4,"ANN - 3 capas ocultas. Activación: tanh")
ann_tanh_4 = create_data_frame("tanh_4.csv")
ann_tanh_4 = add_ranges_to_data(ann_tanh_4,4,"ANN - 4 capas ocultas. Activación: tanh")
svm512 = create_data_frame("512x16-svm.csv")
svm512 = add_ranges_to_data(svm512,4,"SVM")
all_data = rbind(ann_tanh_2,ann_tanh_3,ann_tanh_4,svm512)

p = create_box_plot(all_data,title = "Escalado en tareas\nComparación entre ANNs con activación tanh",subtitle = "ANN de 2, 3 y 4 capas ocultas con activación tanh",x_title = "Rangos de tareas",y_title = "Diferencia en makespan en (%)",Y = all_data$diff_porcentual)
ggsave("comparacion_anns_tanh.png",width = 25, height = 15, units = "cm",dpi = 300)

## ACTIVACION IDENTITY:
ann_identity_2 = create_data_frame("identity_2.csv")
ann_identity_2 = add_ranges_to_data(ann_identity_2,4,"ANN - 2 capas ocultas. Activación: identity")
ann_identity_3 = create_data_frame("identity_3.csv")
ann_identity_3 = add_ranges_to_data(ann_identity_3,4,"ANN - 3 capas ocultas. Activación: identity")
ann_identity_4 = create_data_frame("identity_4.csv")
ann_identity_4 = add_ranges_to_data(ann_identity_4,4,"ANN - 4 capas ocultas. Activación: identity")
svm512 = create_data_frame("512x16-svm.csv")
svm512 = add_ranges_to_data(svm512,4,"SVM")
all_data = rbind(ann_identity_2,ann_identity_3,ann_identity_4,svm512)

p = create_box_plot(all_data,title = "Escalado en tareas\nComparación entre ANNs con activación identity",subtitle = "ANN de 2, 3 y 4 capas ocultas con activación identity",x_title = "Rangos de tareas",y_title = "Diferencia en makespan en (%)",Y = all_data$diff_porcentual)
ggsave("comparacion_anns_identity.png",width = 25, height = 15, units = "cm",dpi = 300)

## COMPARACION 2 CAPAS TANH e IDENTITY
ann_tanh_2 = create_data_frame("tanh_2.csv")
ann_tanh_2 = add_ranges_to_data(ann_tanh_2,4,"ANN - 2 capas ocultas. Activación: tanh")
ann_identity_2 = create_data_frame("identity_2.csv")
ann_identity_2 = add_ranges_to_data(ann_identity_2,4,"ANN - 2 capas ocultas. Activación: identity")
svm512 = create_data_frame("512x16-svm.csv")
svm512 = add_ranges_to_data(svm512,4,"SVM")
all_data = rbind(ann_tanh_2,ann_identity_2,svm512)

p = create_box_plot(all_data,title = "Escalado en tareas\nComparación entre ANNs de 2 capas ocultas",subtitle = "ANN entrenada con activación tanh y \nANN entrenada con activación identity",x_title = "Rangos de tareas",y_title = "Diferencia en makespan en (%)",Y = all_data$diff_porcentual)
ggsave("comparacion_anns_2_capas_tanh_identity.png",width = 25, height = 15, units = "cm",dpi = 300)
