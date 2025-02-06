#This a lesson on type casting, input()
#This is the process of converting one variable to another
#str(), int(), float(), bool()
name = "olayokun Ololade Emmmanuel"
Age = 24
Gpa = 4.51
is_student = False

print(type(Age))
print(type(is_student))

#now we show how to convert variables
#we can say
Age = float(Age)
gpa = int(Gpa)
print(Age)#this will give us 24.0
print(gpa)#this will covert the float 4.51 to the integer 4 
is_student = str(is_student)
name = bool(name)
print(is_student)#this is will give us a string "False"
print(name)#this will give us true, but if the "" is empty it will give us false

#input()-- a function that prompts the user to enter data
#Lets use an input to collect and print name

name = input("Whats your name ?: ")
Age2 = input("How old are you ?: ")
print(f"hello {name}")
print(f"You are {Age2} years old")
#all input placed will be in the string data type so we cants make calculations with number input
#to solve this problem we typecast the input function
next_age = int(input("Whats your current age?: "))
next_age = next_age + 1
print(f"you will be {next_age} next year")

#Now lets calculate the Area of a rectangle
#Area of a rectangle is length multiplied by the width
length = float(input("Enter the length :"))
width = float(input("Enter the width :"))
Area = length * width
print(f"The Area of this rectangle is {Area}")


#Now we are going to create a shopping cart
item = input("What item would you like buy: ") 
price = float(input("Whats the price of the item:$ "))
quantity = int(input("How many of the item do you want to buy: "))
total = price * quantity
print(f"You are to pay ${total} for {quantity} {item}s")