#string method
string_input = input("enter a word of a sentence: ")
#to get the length of a string we use "len()" method
print(len(string_input))#gives us the length of the input string

#to find character within a string we use find() method
print(string_input.find(" "))#it will find the first index where space " " is located
print(string_input.rfind("o"))#it will find the last index where space " " is located
#if it cant find the character it will return -1

#capitalize() method is use to capitalize the first letter of a string
print(string_input.capitalize())
print(string_input.upper())#to turn everything to capital letter 
print(string_input.lower())#to turn everything to lowercase letter
print(string_input.isdigit())#To check if all the characters are digits
print(string_input.isalpha())#To check if all the characters are alphabets
print(string_input.count("o"))#counts the amount of "o" character in the string
print(string_input.replace(" ", "x"))#its gonna replace all the " " with "x" in the string


#To get a full list of all this methods we use help()
print(help(str))

#to validate a username i python
#name must not be more than 12 characters 
#must not contain spaces
#name must not contain digit

username = input("Enter your preferred user name: ")

if len(username) > 12 :
    print(f"{username} is more than 12 characters")
elif username.count(" ") >=1:#(not username.find(" ") ==-1)
    print(f'username should not contain spaces')
elif not username.isalpha():
    print("username should not contain digit")


#INDEXING IN PYTHON
#this is used to fish out the elements of a stringS by indexes

Example = "123456789"
print(Example[0])
#to print from a certain set of indexes 
print(Example[0:4])#this will give us 1234 (i.e from index 0 - index 3)
print(Example[4:])#this will print from index 4 - the last index
#if i had used [4:9] it would have excluded index 9

#if we want to print the index from backwards we use negative indexes
print(Example[-1])#his will give us 9
print(Example[-4:])#this will give us the last four digits 6789

#now we use the step indexes function
print(Example[::2])#this will skip one index on each step(13579)
print(Example[::3])#this will skip two indexes on each step(147)

#to reverse a string we use step  [::-1]
print(Example[::-1])
# to reverse with step
print(Example[::-2])


#FORMAT SPECIFIERS :changes format of the output based on the inserted flag
#Examples
price1 = 34.5389
print(f"the price of the product is ${price1:.2f}")#i.e 2 decimal places for float
print(f"the price of the product is ${price1:10}")#creates 10 space container
print(f"the price of the product is ${price1:>10}")#justify to the left ('<10' will justify to the right)
print(f"the price of the product is ${price1:^10}")#justify to the center