import time
#function = block of reusable code 
    #place () after he function name to invoke it

#for example we want to print something three times without copy and paste or using loop
def happy_birthday(name, age):
    print(f"happy birthday to you {name}")
    print("How old are you now ?")
    print(f"You are {age} years old")
    print()

#Lets say we want to tell three different people
happy_birthday("Ololade", 24)
happy_birthday("Zoe", 22)
happy_birthday("Jeremy", 23)

#we create a function to generate an invoice
def display_invoice(username, amount, due_date):
    print(f"Hello {username}")
    print(f"Your bill of ${amount: 2f} is due: {due_date} ")

display_invoice("Emmanuel", 39.999, "02/25")


#return = statement used to end a function
#           and send a result to the caller 
z = 0
def add_num(x, y):
    z = x + y 
    return z

def subtract_num(x, y):
    z = x - y
    return z

def divide_num(x, y):
    z = x / y
    return z

def multiply_num(x, y):
    z = x * y
    return z

print(add_num(6, 5))
print(divide_num(57,3))


#Lets use a function to print full name
def  print_name(first, middle, last):
    first = first.capitalize()
    middle = middle.capitalize()
    last = last.capitalize()
    return first + " " + middle + " " + last

full_name = print_name("ololade","emmanuel","olayokun")
print(full_name)


#We are going to cover DEFAULT argument
#This are arguments for certain parameters and it reduce the number of arguments
#there are other type of arguments "position","keyword","arbitrary"
#We are going to create a function to get net price for buying a item using tax and discount
def net_price(item_price,discount,tax): #using position arguments
    return item_price *(1 - discount)*(1 + tax)
print(net_price(500,0.1,0.06))

def net_price(item_price,discount=0.2,tax=0.05): #using default arguments arguments
    return item_price *(1 - discount)*(1 + tax)
print(net_price(500))#the default arguments dont need to be stated again



#We can create a counter program using the timer 
#first we import the time function "import time" on the first line of this page
#def count(start=0, end):  #This will give us error, you cannot out a default argument before a position argument
def count(end, start=0): #"start" is the default argument
    for x in range(start, end+1):
        print(x)
        time.sleep(1)
    print("DONE")

#count(0, 10)
count(5)



#Keyword argument = are arguments preceded by an identifier
#                   helps with readability, The order it ias written in doesn't matter

def print_greetings(greeting, title, first,last):
    print(f"{greeting} {title} {first} {last}")

#print_greetings(last="Olayokun",first="Ololade",title="Mr","hello" ) #(ERROR)keyword arguments cannot appear before position arguments
print_greetings("hello" ,last="Olayokun",first="Ololade",title="Mr")#the order at which the parameters are written doesnt matter 

#BUILT IN KEYWORD ARGUMENTS
print("1","2","3","4","5",sep=" ")#sep= built in keyword function to separate by " "

#Lets build a program to generate phone number
def get_phone(country, area, first, last):
    return f"{country}-{area}-{first}-{last}"
phone_num = get_phone(area="090",last=9676, country=+234, first=6861)

print(f"Your phone number is{phone_num}")



#This is arbitrary arguments that means varying arguments
# *args = allows you to pass multiple non-key arguments and stores them in a tuple
# **kwargs = allows you pass multiple keyword-arguments and stores them in a tuple
#            (*) is the unpacking operator
# EXAMPLE 1
def add(*args): #the name "args" can be changed to what ever you like
    print(type(args)) # to prove tha args is a tuple
    total = 0
    for arg in args:
        total = total + 1
    return total


print(1,2,3,4,5)

#EXAMPLE 2
#a program to print the name of a person
def Oruko(*names): #the name "names" can be changed to what ever you like
    print(type(names)) # to prove tha args is a tuple
    for name in names:
        print(name, end=" ")

print(Oruko("Dr","olayokun","Ololade","Emmanuel"))


# NOW WE USE KWARGS
#this **kwargs put arguments into a dictionary
def print_address(**kwargs): #the name "names" can be changed to what ever you like
    for key, value in kwargs.items():# This to prove that the arguments are placed in a dictionary
        print(f"{key}: {value}")

print(print_address(street = "Amosun",
                    city = "Obadore",
                    state = "lagos",
                    postal_code= "10025"))


#Now combine both *args and **kwargs in one example
def Details(*names, **keywords): #the name "names" and "keywords" can be changed to what ever you like
#def Details(**keywords,*names) #This will give us error because "kwargs" cant come before "args" 
    for name in names:
        print(name, end=" ")
    print()
    for key, value in keywords.items():
        print(value,end=" ")
    print()
    #to check if a key is in the kwargs dictionary
    check = "apt" in keywords
    print(check)#This will give us true as "apt" is in "keywords"
    check1 = "pobox" in keywords
    print(check1) #This will give us false as "pobox" is not in "keywords"

print(Details("Dr","olayokun","Ololade","Emmanuel",
            street = "Amosun",
            apt = "apartment 103",
            city = "Obadore",
            state = "lagos",
            postal_code= "10025"))

