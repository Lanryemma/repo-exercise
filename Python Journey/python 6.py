import time
#LOOPS WHILE LOOP,FOR LOOP, 
"""print("")
name = input("Enter your name: ")
while name == "":
    print("you didn't enter any name ")
    name = input("Enter your name: ")    

print(f"hello {name}")

#example 2
print("")
agee = int(input("Enter your age: "))
while agee <=0 :
    print("you didn't enter a valid age ")
    agee = int(input("Enter your age: "))    

print(f"You are {agee} years old")

#Example 3
print("")
food = input("Enter your best food('q' to quit): ")
while  not food == "q":
    print(f"Would you like to buy some {food}")
    food = input("Enter your best food: ")

print("bye then")

#Example three
print("")
number = int(input("Enter a number from 1 - 10: "))

while number <1 or number >10:
    print("The number you entered is not valid")
    number = int(input("Enter a number from 1 - 10: "))

print(f"{number} is valid")"""



#PROGRAM FOR COMPOUND INTEREST
#FOR THIS PROGRAM WE WILL NEED THE PRINCIPLE, RATE AND TIME 
"""print("")
principle = 0
rate = 0
time = 0

while principle <=0:
    principle =float(input("Enter your principle for investment: "))
    if principle <=0:
        print(f"{principle} cannot be invested ")
    else:
        print(f"${principle} will be invested")

while rate <=0:
    rate =int(input("Enter your rate for investment: "))
    if rate <=0:
        print(f"{rate}% is not a valid rate ")
    else:
        print(f"{rate}% of investment in profit")

while time <=0:
    time =int(input("Enter time period in years for investment: "))
    if time <=0:
        print(f"{time} years is an invalid time period ")
    else:
        print(f"${time} years will be the waiting period ")

compound_interest = principle*(pow(1 + (rate/100), time))

print(f"${principle} compound interest after {time} years at {rate}% rate is {round(compound_interest, 2)}")"""




#FOR LOOPS
#used to execute a block of cod a fixed number of times 

#Example 1 (to iterate over a range function)
"""for x in range(1, 11, 2):# "1" is the start, "11" is the end, "2"is the step value of count
    print(x)
#we can also reverse the count
print("")
for x in reversed(range(1, 11, 2)):
    print(x)

#no we iterate over strings
print("")
word ="1234-5678-91011"
for y in word:
    print(y)

#How to make the for loop skip a step
print("")
for z in range(1, 21):
    if z == 14:
        continue
    else:
        print(z)
#How to end the loop
print("")
for z in range(1, 21):
    if z == 14:
        break
    else:
        print(z)


#CREATING A COUNT DOWN DOWN APP
#first we import the time method from python
my_time = int(input("Enter count down time: "))
for x in range(0, my_time):#this will give us (0,1,2,3,4, TIME'S UP) if my_time=5
    print(x)
    time.sleep(1)

print("TIME'S UP")
# to reverse it 
for x in range(my_time, 0, -1):#or [reversed(range(0, my_time))](4,3,2,1, 0 TIME'S UP)
    print(x)
    time.sleep(1)

print("TIME'S UP")

#To create a digital clock program
for x in range(my_time, 0, -1):#this will give us (0,1,2,3,4, TIME'S UP)
    seconds = x % 60
    minutes = int(x / 60)% 60
    hours = int(x / 3600)
    print(f"{hours:02}:{minutes:02}:{seconds:02}")
    time.sleep(1)

print("TIME'S UP")"""

"""x = 600
seconds = x % 60
minutes = int(x / 60)% 60
hours = int(x / 3600)

print(seconds)
print(minutes)
print(hours)"""


#NESTED LOOPS
for t in range(3):
    for y in range(1,10):
        print(y,end=" ") #'end=""' uis to help arrange the results i an horizontal manner with space " " in between 


#create a rectangle with roles and column
print("")
rows = int(input("Enter number of rows: "))
columns = int(input("Enter number of columns: "))
symbols = input("Enter symbol/string: ")
for t in range(rows):
    for r in range(columns):
        print(symbols,end=" ")
    print()