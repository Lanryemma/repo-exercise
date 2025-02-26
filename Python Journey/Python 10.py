#Iterables = An Object/collection that can return its elements one at a time
#              allowing it to be iterated over in a loop

#EXAMPLES
list = [1,2,3,4,5] #Iterable 1 --- Lists
tuples = (1,2,3,4,5)#Iterable 2 ----Tuple
Sets = {1,2,3,4,5} #Iterable 3 ---- Sets (they are not reversible)
Strings= "OloladeEmmanuel" #Iterable 4 ----strings
"""Dictionary = {"A":1, "B":2, "C":3,"D":4,"E":5} #Iterable 5 ----dictionary

letter = input("Enter an alphabet: ").upper()
if letter in Dictionary:
    print(f"{letter.upper()} is for {Dictionary[letter.upper()]}")
else:
    print(f"{letter.upper()} is not present in the dictionary")"""


#---------------------------------------------------------------------------------------------------
#List comprehension =a concise way to write a list in python 
#                       compact and easier to read then traditional loops
#                      [expression for values in iterable if condition]


#This is a normal code code to generate a list buy using range
double= []
for x in range(1, 11):
    double.append(x* 2)

print(double)

#now we put this code into one line by using list comprehension
double1 = [x*2 for x in range(1,11)]
print(double1)

#Example 3
"""double2 =[]
for y in range(1, 11):
    double2.append(y* y)

print(double2)"""
#The code above can be written as 
double2 = [y*y for y in range(1, 11)]
print(double2)


#Now we use string example 
fruits = ["apple","orange","mango","berry"]
for fruit in fruits:
    print(fruit.upper())

#now we use the list comprehension form
fruits1 = [fruit.upper() for fruit in  ["apple","orange","mango","berry"]]
print(fruits1)
print()
#or we code leave he definition outside
fruits2 = ["apple","banana","mango","pawpaw"]
fruits2 = [fruit[1] for fruit in  fruits2]
print(fruits2)


#Now we test it on conditions
numbers = [1,-2,3,-4,5,-6,7,-8]
positive_nums = [num for num in numbers if num >= 0]
negative_nums = [num for num in numbers if num < 0]
even_nums = [num for num in numbers if num%2 == 0]
odd_nums = [num for num in numbers if num%2 == 1]
print(positive_nums, negative_nums,even_nums,odd_nums)



#-------------------------------------------------------------------------------------------------------------------
#Match-case statement ("switch" in java script): An alternative to using many"elif"statement
#                           Execute some code if a value matches the case
#                           Benefits: cleaner and syntax is more readable

#Example 1 print what day it is depending on the number entered
def day_of_week (day):
    match day: # instead of using if statement
        case 1:
            return "Today is Sunday"
        case 2:
            return "Today is Monday"
        case 3:
            return "Today is Tuesday"
        case 4:
            return "Today is Wednesday"
        case 5: # instead of using elif statement
            return "Today is Thursday"
        case 6:
            return "Today is Friday"
        case 7:
            return "Today is saturday"
        case _: # instead of using else statement
            return "This day does not exist"


print(day_of_week(5))

# Example 2
def weekend (day):
    match day: # instead of using if statement
        case "sunday":
            return "Today is Weekend"
        case "monday":
            return "Today is not weekend"
        case "tuesday":
            return "Today is not weekend"
        case "wednesday":
            return "Today is not weekend"
        case "thursday": # instead of using elif statement
            return "Today is not weekend"
        case "friday":
            return "Today is weekend"
        case "saturday":
            return "Today is weekend"
        case _: # instead of using else statement
            return "This day does not exist"

print(weekend("tuesday").lower())

#To shorten this code
def weekend1 (day):
    match day: # instead of using if statement
        case "sunday"|"saturday"|"friday":
            return True
        case "monday"|"tuesday"|"wednesday"|"thursday":
            return False
        case _:
            return False

print(weekend1("saturday"))