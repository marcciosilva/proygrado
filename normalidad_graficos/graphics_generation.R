setwd("~/proygrado/normalidad_graficos")
install.packages("plotly",dependencies=TRUE)
install.packages("pracma",dependencies=TRUE)
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

generate_median_min_max_chart = function(calcs,cateogry_values,message){
  x = calcs$rangos
  y1 = calcs$min
  y2= calcs$median
  y3 = calcs$max
  data = data.frame(x,y1,y2,y3)
  p <- plot_ly(data = data, x = ~x, y = ~y3, type = 'bar', name = 'Máximo', marker = list(color = 'rgb(49,130,189)')) %>%
    add_trace(y = ~y2, name = 'Mediana', marker = list(color = 'rgba(152, 0, 0, .8)')) %>%
    add_trace(y = ~y1, name = 'Mínimo', marker = list(color = 'rgb(204,204,204)')) %>%
    layout(xaxis = list(title = "Medianas en escalado", tickangle = -45,
                        categoryorder = "array",
                        categoryarray = cateogry_values),
           yaxis = list(title = ""),
           margin = list(b = 100),
           barmode = 'group',
           legend = list(x = 0.5, y = 0.9),
           title = paste("Medianas por rangos en escalado\n",message))
}

median_analysis = function(data,message){
  entry = 1
  calcs = data.frame(matrix(vector(),0,3))
  for (i in c(200,400,600,800,1000,1200)){
    names(calcs) = c("median","max","min")
    from = i - 200
    to = i
    values_to_observe = data[,4] < to & data[,4] >= from
    new_data = data[values_to_observe,7]
    calcs = rbind(calcs, c(median(new_data),max(new_data),min(new_data)) )
  }
  categry_values = c("#maquinas+1:199","200:399","400:599","600:799","800:999","1000:1024")
  calcs = cbind(calcs,categry_values)
  names(calcs)[4] = "rangos"
  p = generate_median_min_max_chart(calcs,categry_values,message)
  return(p)

}

median_analysis_for_accuracy = function(data,message){
  entry = 1
  calcs = data.frame(matrix(vector(),0,3))
  for (i in c(200,400,600,800,1000,1200)){
    names(calcs) = c("median","max","min")
    from = i - 200
    to = i
    values_to_observe = data[,4] < to & data[,4] >= from
    new_data = data[values_to_observe,3]
    calcs = rbind(calcs, c(median(new_data),max(new_data),min(new_data)) )
  }
  categry_values = c("#maquinas+1:199","200:399","400:599","600:799","800:999","1000:1024")
  calcs = cbind(calcs,categry_values)
  names(calcs)[4] = "rangos"
  p = generate_median_min_max_chart(calcs,categry_values,message)
  return(p)
  
}


ann128 = create_data_frame("128x4-ann.csv")
svm128 = create_data_frame("128x4-svm.csv")
comparacion_ann_svm_128 = create_electrocardiogram(ann128,svm128,"ann - 2 capas ocultas","svm","128x4")
max_median_min = median_analysis(ann128,"Para ANN entrenada con dimensión 128x4")
max_median_min
accuracy_plot = median_analysis_for_accuracy(ann128,"Para ANN entrenada con dimensión 128x4")
accuracy_plot

p <- subplot(p1, p2, p3, , titleX=TRUE, nrows = 2) %>%
  layout(title = "Walmart Store Openings by Year",
         xaxis = list(domain=list(x=c(0,0.5),y=c(0,0.5))),
         scene = list(domain=list(x=c(0.5,1),y=c(0,0.5))),
         xaxis2 = list(domain=list(x=c(0.5,1),y=c(0.5,1))),
         showlegend=FALSE,showlegend2=FALSE)

ann512 = create_data_frame("512x16-ann.csv")
svm512 = create_data_frame("512x16-svm.csv")
grande2capas = create_electrocardiogram(ann512,svm512,"ann - 2 capas ocultas","svm","512x16")
grande2capas

ann512_3capas = create_data_frame("512x16-ann-3capas.csv")
grande3capas = create_electrocardiogram(ann512_3capas,svm512,"ann - 3 capas ocultas","svm","512x16")
grande3capas

ann512_4capas = create_data_frame("512x16-ann-4capas.csv")
grande4capas = create_electrocardiogram(ann512_4capas,svm512,"ann - 4 capas ocultas","svm","512x16")
grande4capas



  calculate_accuracy_plot = function(data,message){
    fited_y_for_data = create_polynomial_fit(3,data[,4],data[,3])
    p = plot_ly(x = data[,4], y = data[,3], mode = 'markers', marker = list(size = 2)) %>%
      #(y = fited_y_for_data, mode = 'lines',line = list(color = 'red', width = 1),showlegend = FALSE) %>%
      layout(xaxis = list(title = "Medianas en escalado"),
             yaxis = list(title = ""),
             margin = list(b = 100),
             barmode = 'group',
             legend = list(x = 0.5, y = 0.9),
             title = paste(title="Accuracy en clasificación para ANN entrenada con instancias de 128x4\n",message))
    return(p)
  }

