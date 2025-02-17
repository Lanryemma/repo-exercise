#collection is a variable used tp store multiple value 
#list = [] Ordered and changeable, duplicates ok
#set = {} unOrdered and Immutable, doesn't duplicates 
#Tuple = () Ordered and unchangeable, duplicates ok, faster

"""fruits =["apple", "orange","banana","coconut"]
print(fruits[3])
print(fruits[0:3])#to print from index 0 - 3
print(fruits[::2])#this will skip the next element ['apple', 'banana']
print(fruits[::-1])#print it in reverse

# to get all the method we can use for this list collection we use dir(fruits)
#print(dir(fruits))
#print(help(fruits))#to see how to use all the methods available to this list)
print(len(fruits))#to get the length of the list

#we can also change the elements of the list
#fruits[0] = "pawpaw"
#print(fruits) #this will give us ['pawpaw', 'orange', 'banana', 'coconut']
#fruits.append("mango") #adds mango to the end of the list
#fruits.remove("apple") #removes apple from the list
#fruits.insert(0, "berry") #inserts "berry at index 0 position i the list"
#fruits.sort() #sorts the list in alphabetical order
#fruits.reverse() #reverses the list
#fruits.clear() #Clears the list
#print(fruits.index("orange")) #to get the index of orange on the list
#fruits.count("orange") #to count the amount of time orange appeared on the list



#WE MOVE TO SET
#Sets are {} unOrdered and Immutable, doesn't duplicates 
fruits1 ={"apple", "orange","banana","coconut"}
print(fruits1)
#print(fruits1[0]) #This will give us error as set is unordered so its cant have indexes
#print(dir(fruits1)) to see all the methods available for this set
#print(help(fruits1))to see details on how to use this methods
print("pineapple" in fruits1) #this will give false since pineapple is not in the set
fruits1.add("mango")
fruits1.remove("apple")
fruits1.pop() #it the remove the last value in the set, its random since there eis no order
#fruits1.clear() # clears the set


#NOW WE MOVE TO TUPLE 
fruits2 =("apple", "orange","banana","coconut", "orange")
#print(dir(fruits1)) to see all the methods available for this TUPLE
#print(help(fruits1))to see details on how to use this methods
print(fruits2.count("orange")) #to count the amount of time orange appeared on the tuple
print(len(fruits2))#to get the length of the tuple
print(fruits2.index("orange")) #to get the index of orange on the tuple
print("pineapple" in fruits2) #this will give false since pineapple is not in the tuple

for fruit in fruits2:
    print(fruit)"""




#We are to create a shopping cart program using list collection
"""foods = []
prices = []
total = 0

print()
while True:
    food = input("Enter a food to buy (q to quit): ")
    if food.lower() == "q":#the lower() function is to allow for both small and capital letter (Q/q)
        break
    else:
        price = float(input("Enter the price of the goods: "))
        foods.append(food)
        prices.append(price)

print("----YOR CART-------")

for price in prices:
        total = total + price

for x in range(len(foods)):
    print(f"{foods[x]} --- ${prices[x]}")# or print(f"{foods[x]} --- ${prices[x]}, end=" ") to appear horizontal

print(f"Total price of food items = ${total} ")
#print(f"{food} --- ${price}")"""


#------------------------------------------------------------------------------------------------------------------------------------------
#2D LIST IS A LIST INSIDE ANOTHER LIST (EXAMPLE BELOW)

Fruits = ["orange","apple","mango"]
vegetables = ["Onion","cucumber","carrot"]
meats =  ["chicken","Turkey","fish"]

Groceries = [Fruits, vegetables,meats]

print(Groceries[0][2])#this will give us "mango"

#2D list can also be arranged like this
Groceries1 = [["orange","apple","mango"],["Onion","cucumber","carrot"],["chicken","Turkey","fish"]]
print(Groceries1[0][2])#this will still give us "mango"

#to iterate over the 2D list
for list in Groceries1:
    for items in list:
        print(items, end=" ")
    print()


#2D tuple (print a key pa using 2D tuple)
key_pad = ((1,2,3),(4,5,6),(7,8,9),("*",0,"#"))

for row in key_pad:
    for num in row:
        print(num, end=" ")
    print()



#-------------------------------------------------------------------------------------------------------------------------
#we are going to create a quiz game in  python
"""questions = (("Whats 63/3 ?"),
             ("Whats 24 x 5 ?"),
             ("whats 9 x 7 ?"),
             ("Whats 321 + 253 ?"),
             ("Whats 726 - 381 ?"))

Options =(("A: 45","B: 32","C: 21","D: 25"),
          ("A: 221","B: 240","C: 160","D: 120"),
          ("A: 51","B: 63","C: 45","D: 77"),
          ("A: 600","B: 482","C: 574","D: 552"),
          ("A: 345","B: 322","C: 211","D: 525"))

answers = ("C","D","B","C","A")
guesses = []
score = 0
question_num = 0

for question in questions:
    print("-----------------------------------")
    print(question)
    for option in Options[question_num]:
        print(option)
    guess = input('Enter (A, B, C, D): ').upper()#incase the user enter small letter 
    guesses.append(guess)
    if guess == answers[question_num]:
        score = score + 1
        print("CORRECT")
    else:
        print("INCORRECT")
        print(f"{answers[question_num]} is the right answer")
    question_num = question_num + 1

print("-----------------------------------")
print("-------------RESULTS---------------")
print("-----------------------------------")

print("You guessed: ",end=" ")
for ges in guesses:
    print(ges, end=" ")
print()

print("The answers are: ",end=" ")
for an in answers:
    print(an, end=" ")
print()

percent_score = (score /len(questions))*100
print(f"You scored {percent_score}%")"""




#-------------------------------------------------------------------------------------------------------
#dictionary = a collection of {key: value} pairs
#               ordered and changeable. No duplicates

languages = {"USA":"English",
            "Germany":"German",
            "Finland":"Finish",
            "Sweden": "Swedish"}

#to get the value using the key
print(languages.get("USA"))
#we can use if statement to verify if the key is in the dictionary
if languages.get("Norway"):
    print("that language is not in the database")
else:
    print("that language is in the database")

#we can also add a new key-value pair
languages.update({"France":"French"})  #we just inserted france
languages.update({"Finland":"Yoruba"})  #we just changed finland language in the dictionary
#languages.pop("USA")  #we just removed usa from the dictionary
#languages.popitem()  #we just removed the latest addition to the dictionary (France)
#languages.clear()  #to clear the dictionary

#to get the keys only we use the key method 
keys = languages.keys()
print(keys)
print()
#we can iterate through the keys
for key in keys:
    print(key)


print()
#to get the values only we use the key method 
values = languages.values()
print(values)
#we can iterate through the values
for key in keys:
    print(key)


print()
#to get the items we use the items method 
items = languages.items()
print(items)
print()
#we can iterate through the values
for key, value in items:
    print(f"{key}: {value}")





#This is a program for a concession stand in a cinema using Dictionary

menu = {"pizza": 3.00,
        "nachos": 4.00,
        "fries": 2.00,
        "soda": 3.50,
        "chips": 5.10,
        "popcorn": 6.00,
        "pretzel": 4.50,
        "lemonades": 2.70}

cart =[]
item_price = []
total =0
#Now we display the list for the users

print("-----------MENU-----------")
for key,value in menu.items():
    print(f"{key:10} : ${value}")#"{key:10}" this is to add 10 spaces after the key
print("--------------------------")

# to allow users to load available foods to their cart
while True:
    food = input("Select items from the menu(Q/q to quit): ").lower()
    if food == "q":
        break
    elif not menu.get(food) == None:
        cart.append(food)


for item in cart:
        print(f"{item} ----${menu.get(item)}")
        total = total + menu.get(item)

print(f"total price is: ${total}")