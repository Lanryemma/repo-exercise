#This is to practice if, elseif and else statement
age = int(input("Enter your Age: "))

if age >=18 and age < 100:
    print("you can sign up")
elif age > 100:
    print("You are too old to sign up")
elif age <= 0:
    print("You haven't been born yet")
else:
    print("You are to young to sign up")
    
#This is an example for yes/no
response = input("would you like some food (Y/N): ")

if response == "Y" or response == "y":
    print("You can have some food")
elif response == "N" or response == "n":
    print("call me later if you change your mind")
else:
    print("answer with either Y/N")
    
#if we use the boolean variables for if and else
if_for_sale = True
if if_for_sale :
    print("This item is for sale")
else:
    print('This item is nit for sale')
    

#This is a calculator with if and else statement 
Operator = input("Enter mathematical operator(+,-,/,*): ")
if  Operator == "+" or Operator == "-" or Operator == "/" or Operator == "*":
    num1 = float(input("enter first number: "))
    num2 = float(input("enter second number: "))

    if Operator == '+':
        result = num1 + num2
    elif Operator == "-":
        result = num1 - num2
    elif Operator == "/":
        result = num1 / num2
    elif Operator == "*":
        result = num1 * num2

    print(round(result))
elif Operator != "+" or Operator != "-" or Operator != "/" or Operator != "*":
    print(f"{Operator} is not a mathematical operator")


#This is an exercise to create temperature converter
unit = input("is the temperature in celsius or fahrenheit? (C/F): ")
if unit == "c" or unit =="C" or unit == "f" or unit == "F":
    temp = float(input("enter the temperature value: "))
    if unit == "c" or unit == "C":
        result = round(((9*temp)/5)+ 32, 1)
        print(f"{temp} celsius is {result} fahrenheit")
    elif unit == "f" or unit == "F":
        result = round(((temp-32)*5)/9, 1)
        print(f"{temp} fahrenheit is {result} celsius")
elif unit != "c" or unit !="C" or unit != "f" or unit != "F":
    print(f"{unit} is not a valid unit indicator")


#one line conditional expression 
num = 5
num1= 6
age = 25

print("positive" if num >0 else "negative")#positive
print("even number" if num1%2 == 0 else "odd number")#odd number
print("adult" if age >= 18 else "Child")#Child

user = "Admin"
access_level = "full access" if user == "Admin" else "restricted access"
print(access_level)