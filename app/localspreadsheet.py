# CSV Code

import csv

with open('Local_Python_Project_Sheet - Sheet1.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
        append.