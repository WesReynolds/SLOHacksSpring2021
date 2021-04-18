library(ggplot2)
library(tidyverse)
library(rpart)
library(rpart.plot)
library(dplyr)


linear_output = function(data, x, y, xlabel, ylabel, title){
  x = data[,x]
  y = data[,y]
  
  mx = coef(summary(lm(y~x)))["(Intercept)", "Estimate"]
  b = coef(summary(lm(y~x)))["x", "Estimate"]
  r2 = summary(lm(y~x))$adj.r.squared
  
  df = data.frame(mx, b, r2)
  
  write.csv(df, "colm.csv")
  
  ggplot(data, aes(x, y)) +
    geom_point() +
    geom_smooth(method = "lm", se = FALSE, formula = y ~ x) +
    ggtitle(title) +
    xlab(xlabel) + 
    ylab(ylabel)
  
  ggsave(file="lmplot.png")
}

read_csv_lm = function(args){
  data = read.csv(file = args[2])
  r_csv = read.csv(file = args[3])
  
  x = r_csv$x
  y = r_csv$y
  xlabel = r_csv$xlabel 
  ylabel = r_csv$ylabel
  title = r_csv$title

  linear_output(data, x, y, xlabel, ylabel, title)
}

create_train_test <- function(data, size = 0.8, train = TRUE) {
  n_row = nrow(data)
  total_row = size * n_row
  train_sample = 1:total_row
  if (train == TRUE) {
    return (data[train_sample, ])
  } else {
    return (data[-train_sample, ])
  }
}


dt_output = function(data1, target){
  
  variable = c(".")
  
  #Image
  png("dtplot.png")
  data_train <- create_train_test(data1, 0.8, train = TRUE)
  data_test <- create_train_test(data1, 0.8, train = FALSE)
  
  target1 = as.formula(paste(target, paste(variable), sep = "~"))
  tree = rpart(target1, data = data1, cp=.02)
  rpart.plot(tree)
  dev.off()
  
  #Accuracy
  
  prediction = predict(tree, data_test, type='class')
  
  table_mat = table(data_test[[target]], prediction)
  
  accuracy = data.frame(sum(diag(table_mat)) / sum(table_mat))
  names(accuracy) = c("accuracy")
  
  write.csv(accuracy, "accuracy.csv")
}

read_csv_dt = function(args){
  data = read.csv(file = args[2])
  target = args[3]
  dt_output(data, target)
}

kmc_output = function(t_vec, cen, arg){
  
  #values for graph 
  x1 = t_vec$x
  y1 = t_vec$y
  x2 = cen$x
  y2 = cen$y
  
  #label graph 
  xlabel = arg$xlabel
  ylabel = arg$ylabel
  title = arg$title
  
  ggplot() +
    geom_point(data = t_vec, 
               aes(x1, y1)) +
    geom_point(data = cen, 
               aes(x2, y2), color = "red") +
    ggtitle(title) +
    xlab(xlabel) + 
    ylab(ylabel)
  ggsave(file="kmcplot.png")
}
  
read_csv_kmc = function(args){
  t_vec = read.csv(file = args[2])
  cen = read.csv(file = args[3])
  arg = read.csv(file = args[4])
  kmc_output(t_vec, cen, arg)
}

main = function(){
  args = commandArgs(trailingOnly=TRUE)
  if(args[1] == "lm"){
    read_csv_lm(args)
  }else if(args[1] == "dt"){
    read_csv_dt(args)
  }else{
    read_csv_kmc(args)
  }
}
main()

