#Decorator = A function that extends the behavior of another function
#            w/o modifying the base function
#            pass the base function as an argument to the decorator

#            @add_sprinkles
#            get_ice_cream("Vanilla")

def add_sprinkles(func):#this is a decorator function to add sprinkles to an ice-scream when invoked
    def wrapper():
        print("You added sprinkles ")#🎊
        func()
    return wrapper

def add_chocolate(func):#this is a decorator function to add sprinkles to an ice-scream when invoked
    def wrapper():
        print("You added chocolate ")#🍫
        func()
    return wrapper

@add_sprinkles
@add_chocolate
def get_ice_cream():
    print("Here is your ice-cream ")#🍨

get_ice_cream()

#To show how to add arguments to a decorator function
def add_peperoni(func):#this is a decorator function to add sprinkles to an ice-scream when invoked
    def wrapper(*args,**kwargs):
        print("You added peperoni ")#🍫
        func(*args,**kwargs)
    return wrapper

@add_peperoni
def get_pizza(flavor):
    print(f"Here is your {flavor} pizza")

get_pizza("large")



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#exception = An event that interrupts the flow of a program
#            (ZeroDivisionError,TypeError, ValueError)
#            1.try, 2.except, 3.finally

#number = int(input("Enter a number: "))
#print(1/number)  #if we enter "0" we will get "ZeroDivisionError"
#                if we enter a string e.g "pizza" we will get "valueError"
# So in order to not let the error bring our program to a halt we use the "1.try, 2.except, 3.finally"

print()
try:
    number = int(input("Enter a number: "))
    print(1/number)
except ZeroDivisionError:
    print("You cant divide by zero you Idiot!!!")
except ValueError:
    print(f"{number} is not a number")
except Exception:#This is to accept any other error we didn't specify error
    print("something went wrong")
finally:#This is executed after all the exception
    #continue #This will tell the interpreter to continue interpreting even after all the exceptions
    print("Try to clean up the error")




