import os
import subprocess
import csv

x = 1
y = 3
xlabel = "Mpg"
ylabel = "Disp"
title = "Linear Analysis of Mpg vs Disp"


def linear_m(x, y, xlabel, ylabel, title, data):
    with open('arg.csv', mode='w') as arg_file:
        arg_csv = csv.writer(arg_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        arg_csv.writerow(["x", "y", "xlabel", "ylabel", "title"])
        arg_csv.writerow([x, y, xlabel, ylabel, title])
    subprocess.run(["Rscript", "DataVizualization.R", "lm", data, "arg.csv"])


def dec_tree(data, target):
    subprocess.run(["Rscript", "DataVizualization.R", "dt", data, target])


def kmc(data, data1, xlabel, ylabel, title):
    with open('arg.csv', mode='w') as arg_file:
        arg_csv = csv.writer(arg_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        arg_csv.writerow(["xlabel", "ylabel", "title"])
        arg_csv.writerow([xlabel, ylabel, title])
    subprocess.run(["Rscript", "DataVizualization.R", "kmc", data, data1, "arg.csv"])


def kmcEigen(data):
    subprocess.run(["Rscript", "DataVizualization.R", "kmcE", data])

#linear_m(x, y, xlabel, ylabel, title, "mtcars.csv")
#dec_tree("titan2.csv", "survived")

#kmc("pcaTraining.csv", "kMeans.csv", xlabel, ylabel, title)

