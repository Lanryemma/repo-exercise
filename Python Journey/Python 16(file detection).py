#Python file detection

import os

#now we try to check if a file exist use relative file path
file_path = "Python Journey/Testfile.txt"#this is relative file part

if os.path.exists(file_path):
    print(f"The location '{file_path}' does exist")
else:
    print("That location doesn't exist")

print()
file_path1 = "C:\\Users\\user\\Desktop" #we had to add "\\" double slash because python sees "\" single slash as as escape command

if os.path.exists(file_path1):
    print(f"The location '{file_path1}' does exist")
else:
    print("That location doesn't exist")

#we can check if its a file or a directory or folder
file_path2 = "Python Journey"

if os.path.isdir(file_path2):
    print("This is a folder/directory")

if os.path.isfile(file_path):
    print("This is a file")



#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Python writing files (.txt, .json, .csv)

txt_data = "I like pizza!!"

file_path3 = "Python Journey/Testfile.txt"
#we can write to external file using  "w" mode
#file_path3 = "C:\\Users\\user\\Desktop\\Python file detection.txt"

with open(file = file_path3, mode ="w") as file:#the "with" open and closes a file automatically and the "w"is a mode to write inside the file
    file.write(txt_data)
    print(f" text file {file_path3} was created")


#we want to know if the file already exist using the "x" mode
#the "x" mode creates a file if it doesn't exist and a pass a file-exist error if it already does 
"""try:
    file_path4 = "C:\\Users\\user\\Desktop\\Python file detection.txt"

    with open(file = file_path4, mode ="x") as file:#the "x" mode will open a file will the file_path name automatically
        file.write(txt_data)
        print(f" text file {file_path4} was created")
except FileExistsError:
    print("This file already exist")"""

#we can add more to our file with the append mode "a" and do it on a new line "\n"
"""try:
    file_path4 = "C:\\Users\\user\\Desktop\\Python file detection.txt"

    with open(file = file_path4, mode ="a") as file:#the "x" mode will open a file will the file_path name automatically
        file.write("\n" + txt_data)
        print(f" text file {file_path4} was created")
except FileExistsError:
    print("This file already exist")"""

#now we try to put a list in a file
employees  = ["Eugene","Squidward", "Spongebob","Patrick"]

try:
    file_path4 = "C:\\Users\\user\\Desktop\\Python file detection.txt"

    with open(file = file_path4, mode ="w") as file:
        #Now we try to write list employees in the file
        #file.write(employees) #This will give us error as we cant write a list in a file 
        #We would have to iterate over it
        for employ in employees:
            file.write(employ +"\n")#"\n" is to print each item on a new line
        print(f" text file {file_path4} was created")
except FileExistsError:
    print("This file already exist")


#now we want to input a json file into the file 

import json

employee ={
    "name": "Spongebob",
    "age": 30,
    "job" : "cook"
}

try:
    file_path5 = "C:\\Users\\user\\Desktop\\Python file detection.json"

    with open(file = file_path5, mode ="w") as file:
        #we use "json.dump" to input data into json files
        #we indent each key value pair by for spaces using "indent="
        json.dump(employee, file, indent=4)
        print(f" text file {file_path5} was created")
except FileExistsError:
    print("This file already exist")



#Now we work with CSV(comma separated value) files
import csv
employee_data = [["Name","Age","Job"],
                 ["Spongebob", 30, "Cook"],
                 ["Patrick", 37,"Unemployed" ],
                 ["Sandy", 27 ,"Scientist"]]

try:
    file_path6 = "C:\\Users\\user\\Desktop\\Python file detection.csv"

    with open(file = file_path6, mode ="w", newline="") as file:#'newline=""' to remove the extra line after each row
        #we use "writer = csv.writer()" to input data into csv files
        #we have to iterate over the list to get the data
        writer = csv.writer(file)
        for row in employee_data:
            writer.writerow(row)
        print(f" text file {file_path6} was created")
except FileExistsError:
    print("This file already exist")





#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Python reading files (.txt, .json, .csv)
file_read = "C:\\Users\\user\\Desktop\\Python file detection.txt"

with open(file= file_read, mode="r") as file:
    content = file.read()
    print(content)

#if the file doesn't exist ,we can try and catch the error
print()
file_pat = "C:\\Users\\user\\Desktop\\Python file detection.txt"
try:
    with open(file = file_pat, mode ="r") as file:
        Content = file.read()
        print(Content)
except FileNotFoundError:
    print("This file does not exist exist")
#if the file  has restricted permission then we will catch the permission error
except PermissionError:
    print("YOu do not have permission tp read this file ")



#IF WE WANT TO READ json FILE
#we start by importing the json module
print()
import json

file_pat1 = "C:\\Users\\user\\Desktop\\Python file detection.json"
try:
    with open(file = file_pat1, mode ="r") as file:
        Content1 = json.load(file)
        print(Content1)
        #we can access each value by their key
        print(Content1["age"])#this will give us 30
        print(Content1["job"])#this will give us "cook"
except FileNotFoundError:
    print("This file does not exist exist")
#if the file  has restricted permission then we will catch the permission error
except PermissionError:
    print("YOu do not have permission tp read this file ")




#IF WE WANT TO READ csv FILE
#we start by importing the csv module
print()
import csv

file_pat2 = "C:\\Users\\user\\Desktop\\Python file detection.csv"
try:
    with open(file = file_pat2, mode ="r") as file:
        Content2 = csv.reader(file)
        for line in Content2:
            print(line)
        #to print specific columns we use []
        """for line in Content2:
            print(line[0])#"[0]"for the first column,"[1]" for second and "[2]" for third"""
except FileNotFoundError:
    print("This file does not exist exist")
#if the file  has restricted permission then we will catch the permission error
except PermissionError:
    print("YOu do not have permission tp read this file ")
