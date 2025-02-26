#PYTHON OBJECT ORIENTED PROGRAMMING
#Object = A "bundle" of related attributes (variables) and method (functions)
#         Ex. phone, cup, book
#         You need a "class" to create many objects
#class = (blueprint) used to design the structure and layout of an object

#Now we design a car Object example
class Car:
    def __init__(self,model, year, color, for_sale):
        self.model = model
        self.year = year
        self.color = color
        self.for_sale =for_sale
#You can take the definition of the Object into another file buy importing it there
# from (whatever the file name of where the object is defined) import (the object name)
# in this case lets say our file name is "object-file"
# we would say "from object-file import Car"

#Now we are gonna look at methods
#These are functions that belong to an object
    def Drive(self):
        print(f"you are driving a {self.color} {self.model}")

    def Stop(self):
        print(f"You have stopped a {self.color} {self.model}")
#Lets create a function to describe the car
    def Describe(self):
        print(f"A {self.year} {self.color} {self.model}")

Car1 = Car("Jeep Rangler", 2023,"red",True)
#we can use the Class Car Object to represent different cars 
Car2 = Car("Chevrolette", 2020,"black",False)
Car3 = Car("Range rover", 2022,"blue",True)


print(Car1)
print(Car1.model)
print(Car1.year)
print(Car1.color)
print(Car1.for_sale)




#Now we make use of the method
Car1.Drive()
Car2.Stop()
Car3.Drive()

Car1.Describe()


#CLASS VARIABLES = Shared among all instances of a class 
#                   Defined outside the constructor
#                   Allow you to share data among all objects created from that class 

#EXAMPLE
class Student:
    
    class_year = 2023 #This is a class variable (They are Defined outside the constructor)
    num_student = 0
    
    def __init__(self,name, age):#(Constructor)
        self.name = name#These are Instances of a class  
        self.age = age
        Student.num_student += 1#The more the instance of the object we create the more the "num_student" will increase

student1 = Student("spongebob",30)
student2 = Student("Patrick",35)
student3 = Student("Ololade",25)
student4 = Student("Jeremy",23)



print(student1.name)
print(student1.age)
print(Student.class_year)#How to easily make sure its a class variable
print(student1.class_year)

print(Student.num_student)#The answer will be "4" because we have four instances
#Now we use it to form a sentence
print(f"My Graduating class of {Student.class_year} has {Student.num_student} students")
print(student1.name)
print(student2.name)
print(student3.name)
print(student4.name)


#---------------------------------------------------------------------------------------------------------------------------------------
#Inheritance =Allows a class to inherit attributes and methods from another class
#             Helps with code reusability and extensibility
#             Class Child(Parent)

class Animal:
    def __init__(self,name):
        self.name = name
        self.is_alive = True
    
    def eat(self):
        print(f"{self.name} is eating")
    
    def sleep(self):
        print(f"{self.name} is sleeping")

class Dog(Animal):
    #Each children can also have their own attributes
    def Speak(self):
        print("dog goes 'woff!!'")

class Cat(Animal):
    def Speak(self):
        print("cat goes 'Meow!!'")

class Mouse(Animal):
    def Speak(self):
        print("mouse goes 'Squik!!'")

dog = Dog("Bingo")
cat = Cat("Garfield")
mouse = Mouse("Micky")

print()
print(mouse.name)
print(mouse.is_alive)
mouse.eat()
mouse.sleep()
mouse.Speak()

print()
print(dog.name)
print(dog.is_alive)
dog.eat()
dog.sleep()
dog.Speak()

print()
print(cat.name)
print(cat.is_alive)
cat.eat()
cat.sleep()
cat.Speak()


#-------------------------------------------------------------------------------------------------------------------------
#multiple inheritance = inherit from more than one parent 
#                       C(A, B)

#multilevel inheritance = inherit from a parent which inherits from another parent
#                         C(B) <- B(A) <- A

class Prey:
    #Prey should have the ability to flee from predators
    def flee(self):
        print("This animal is fleeing")

class Predator:
    #Predator should have the ability to hunt its prey
    def Hunt(self):
        print("This animal is Hunting")

class Rabbit(Prey):
    pass

class Hawk(Predator):
    pass

class Fish(Predator, Prey):
    pass

rabbit = Rabbit()
hawk = Hawk()
fish = Fish()

rabbit.flee()
hawk.Hunt()
fish.flee()
fish.Hunt()


#MULTILEVEL INHERITANCE
class Animal1:
    
    def __init__(self,name):
        self.name = name
        
    
    def eat(self):
        print(f"This {self.name}  is eating ")
    def Sleep(self):
        print(f"This {self.name} is sleeping")


class Prey1(Animal1):
    #Prey should have the ability to flee from predators
    def flee(self):
        print(f"This {self.name} is fleeing")

class Predator1(Animal1):
    #Predator should have the ability to hunt its prey
    def Hunt(self):
        print(f"This {self.name} is Hunting")

class Rabbit1(Prey1):
    pass

class Hawk1(Predator1):
    pass

class Fish1(Predator1, Prey1):
    pass

rabbit1 = Rabbit1("Rabbit")
hawk1 = Hawk1("Hawk")
fish1 = Fish1("Sword-fish")

print()
#as we can see they inherited the eat and sleep attribute from the grandparent "Animal"
rabbit1.eat()
hawk1.Sleep()
fish1.eat()


#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#Super() = Functions used on childe class to call methods from a parent class (superclass).
#          Allows you to extend the functionality of inherited methods

class Shape:#this is the parent class
    def __init__(self,color,is_filled):
        self.color = color
        self.is_filled = is_filled
        
    def describe(self):
        print(f"This shape is {self.color} and {"filled" if self.is_filled == True else "Not filled"}")
            
class Circle(Shape):
    def __init__(self,color,is_filled,radius):
        super().__init__(color,is_filled)
        self.radius = radius
#we can perform method overriding but redefining a function from the parent class in the child class
    def describe(self):
        print(f"its a circle of area {3.142 *self.radius * self.radius}cm^2")
        #super().describe()  (this is to call the parent version of the describe function)
        

class Square(Shape):
    def __init__(self,color,is_filled,width):
        super().__init__(color,is_filled)
        self.width = width
    
    def describe(self):
        print(f"its a square of area {self.width * self.width}cm^2")
        super().describe()  #(this is to call the parent version of the describe function)
        


class Triangle(Shape):
    def __init__(self,color,is_filled,width,Height):
        super().__init__(color,is_filled)
        self.width = width
        self.Height = Height
    
    def describe(self):
        print(f"its a Triangle of area {(self.width * self.Height)/2}cm^2")
        super().describe()  #(this is to call the parent version of the describe function)


#Now lets construct objects
print()
circle = Circle(color="Red",is_filled=True,radius=5)#we used keyword arguments foe more clarity
print(circle.color)
print(circle.is_filled)
print(f"{circle.radius}cm")
circle.describe()

print()
square = Square(color="Blue",is_filled=False,width=7)#we used keyword arguments foe more clarity
print(square.color)
print(square.is_filled)
print(f"{square.width}cm")
square.describe()

print()
triangle = Triangle(color="yellow",is_filled=True,width=6,Height=8)#we used keyword arguments foe more clarity
print(triangle.color)
print(triangle.is_filled)
print(f"{triangle.width}cm")
print(f"{triangle.Height}cm")
triangle.describe()