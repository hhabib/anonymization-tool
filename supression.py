#Author Name : Preethi Josephina Mudialba
#Original Creating Date : Feb 25st 2017
#Last Modification Date : March7th 2017
#Brief Description: Supression 

import pandas
import numpy as np
import csv


def open_file():
    # To read 25th and 26th columns
    io = pandas.read_csv('od2016.csv',sep=",",usecols=(3,4)) 
    print(io)
    x=np.array(io)
    print("Using Numpy to save the data in an array")
    print(x)
    #if you want to skew the values
    #print("weighted sum: where the weights are 1/4 or 3/4")
    #print(np.average(x, axis=1,weights=[1./4, 3./4]))
    
   
def read_csv_file(file, list_columns):
    
    with open('Supressed.csv', 'w') as csvfile:
        c = csv.writer(csvfile,delimiter = ',', quotechar = '|')
        with open(file,'r') as csv_file:
            #reads the CSV file
            csv_reader = csv.reader(csv_file, delimiter = ',', quotechar = '|')   
            headers = next(csv_reader, None)
            c.writerow(headers)
            for row in csv_reader:
                for col in list_columns:
                    temp = str(row[col])
                    #modify the string
                    length = len(temp)-1
 #                   temp = "**" + temp[3:]
#                    row[col] = temp                                         
                    row[col] = "******"
                c.writerow(row)
   
def main():
 #   open_file()
 #   read_csv_file("./od2016.csv", 3)
     list_columns = [14, 15];
     read_csv_file("./od2016.csv", list_columns)
    

main()
