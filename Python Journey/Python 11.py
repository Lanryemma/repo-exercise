#modules = a file containing code you want to include in your program
#           use "import" to include a module (built in or your own)
#           useful to break up a large reusable separate file 

#to see all the modules we use "print(help("modules"))"
#to know all the information about a particular module e.g "math module" 
# we use help("math")

#import math (to import math module)
#import math as m (you can import a module and represent it as something else)
#from math import e  (this is to import only the exponential function "e" from the maths module)
#from math import pi  (this is to import only the pie function "pi" from the maths module)

#NOW WE CREATE OUR OWN MODULE 
import mymodule
show =mymodule.Pi
show1 = mymodule.cube(3)
show2 = mymodule.area(4)
show3 = mymodule.circumference(3.5)
print(show)
print(show1)
print(show2)
print(show3)


#------------------------------------------------------------------------------------------------
#variables scope = where a variable is visible and accessible 
#scope resolution=(LEGB) Local -> enclosed -> Global -> Built - in
def func():
    x = 1 #local variable (local variable comes first in hierarchy of the interpreter)
    def func2():
        x = 2 #Enclosed variable (comes second when python interpreter is trying to choose the value of x)
        print(x)
    print(x)
    func2()

func()
#for global and built-in example

from math import e #this is a built in variable 
e = 5.5 # this is a local variable
print(e)


#-----------------------------------------------------------------------------------------------------------------
#if __name__ == __main__ : (this script can be imported or run standalone)
#                       function and classes in this module can be reused
#                       without the main block of code executing
#                       helps with readability
#                       leaves no global variable
#                        avoids unintended execution/ 

#ex. library = import library for functionality
#               when running library directly, display a help page

def main():
    #your program
    pass
from mymodule import *
print(__name__)

def main():
    print("Main branch innit ")

if __name__ == "__main__":#help to check if you are running this current script
    main()





#------------------------------------------------------------------------------------------------------------------------------------------------
#Python Banking program


"""def show_balance():
    print(f"your bank balance is ${balance} ")

def deposit():
    bal= balance
    dep = float(input("Enter amount you want to deposit: "))
    if dep <=0:
        print(f"${dep} cannot be deposited")
    else:
        print(f"You deposited {dep}")
    return dep 


def withdraw():
    Draw  = float(input("How much would you like to withdraw: "))
    if Draw > balance:
        print("insufficient funds")
    elif  Draw <=0:
        print("amount must be more than 0")
    else:
        print(f"You withdrew {Draw}")
    return Draw



its_running = True
balance = 0

while its_running:
    print("-------------------------")
    print("Banking Progress")
    print("-------------------------")
    print("1.Show balance")
    print("-------------------------")
    print("2.deposit")
    print("-------------------------")
    print("3.withdraw")
    print("-------------------------")
    print("4.Exit")
    print("-------------------------")

    choice = input("Enter your choice (1-4): ")
    
    if choice == "1":
        show_balance()
    elif choice == "2":
        balance = balance + deposit()
    elif choice == "3":
        balance = balance - withdraw()
    elif choice == "4":
        its_running = False
    else:
        print("That is not a valid choice")

print("Thank you have a nice day")"""


import random
#Python slot machine
def spin_row():
    symbols = ["🍒","🍉","🍋","🔔","⭐"]
    
    result = []
    for symbol in  range(3):
        result.append(random.choice(symbols))
    #if we were using list comprehension 
    #return [random.choice(symbols) for symbol in range(3)]
    return result

def print_row(row):
    print("--------------")
    print(f"{row}",end=" ")
    print("--------------")
    #we could also write print("|", join(row))
def get_payout(row, bet):
    if row[0] == row[1] and row[0]== row[2]:
        if row[0] == "🍒":
            return bet * 2
        if row[0] == "🍉":
            return bet * 3
        if row[0] == "🍋":
            return bet * 5
        if row[0] == "🔔":
            return bet * 7
        if row[0] == "⭐":
            return bet * 9
    else:
        return bet * 0
    return 0

def main():
    balance1 = 100
    print("------------------------------")
    print("Welcome to python slot machine")
    print("-----symbols: 🍒🍉🍋🔔⭐----")
    print("------------------------------")

    while balance1 > 0:
        print(f"Current balance: ${balance1}")
        bet = input("Place the amount you want to stake: ")
        if not bet.isdigit():
            print("please enter a digit")
            continue
        
        bet=int(bet)
        
        if bet > balance1:
            print("insufficient funds")
            continue
        
        if bet <= 0:
            print("Bet must be greater than 0")
            continue
        
        
        balance1 -= bet
        
        row = spin_row()
        print("Spinning...\n")
        print_row(row)
        
        payout = get_payout(row, bet)
        print()
        if payout > 0:
            print(f"You won ${payout}")
        else:
            print("Sorry you lost this round")
            print(f"Current balance: ${balance1}")
        
        balance1 += payout
        
        play_again = input("Do you want to spin again? (Y/N): ").upper()
        if play_again != "Y":
            break

    print("-------------------------------------------------")
    print(f"Game over!!!, Your final balance is ${balance1} ")
    print("-------------------------------------------------")

if __name__=="__main__":
    main()