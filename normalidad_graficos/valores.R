
names = c("128x4-ANN-Inter.csv","128x4-SVM-Inter.csv","512x16-ANN-Inter.csv","512x16-SVM-Inter.csv")

for (name in names){
  data <- read.csv(name, header=TRUE, sep=",")
  entry = 1
  calcs = data.frame(matrix(vector(),0,3))
  for (i in c(200,400,600,800,1000,1200)){
    
    names(calcs) = c("median","max","min")
    from = i - 200
    to = i
    values_to_observe = data[,3] < to & data[,3] >= from
    new_data = data[values_to_observe,6]
    calcs = rbind(calcs, c(median(new_data),max(new_data),min(new_data)) )
    #calcs = rbind(calcs,row)
    
  }
  write.csv(calcs, file = paste(name,"valores.csv",sep=""))
}
