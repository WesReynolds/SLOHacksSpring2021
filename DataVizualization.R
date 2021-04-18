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

dt_output = function(data1, target){
  png("dtplot.png")
  target = data1[,target]
  tree = rpart(target~., data = data1, cp=.02)
  rpart.plot(tree, box.palette="RdBu", shadow.col="gray", nn=TRUE)
  dev.off()
}

read_csv_dt = function(args){
  data = read.csv(file = args[2])
  target = args[3]
  dt_output(data, target)
}

read_csv_kmc = function(args){
  t_vec = read.csv(file = args[2])
  k_vec = read.csv(file = args[3])
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

