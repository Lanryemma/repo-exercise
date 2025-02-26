#polymorphism = Greek word that means to "have many forms or faces"
#               poly = Many
#               morphe = Form

#               Two ways to achieve polymorphism 
#               1. Inheritance = An Object could be treated of the same type as the parent class
#               2. "Duck typing" = Object must have necessary attributes/method

#in this example we are going to use abstract methods and we will import it
from abc import ABC, abstractmethod
class Shape:
    
    @abstractmethod
    def Area():
        pass

class Circle(Shape):
    def __init__(self,radius):
        self.radius = radius
    
    def Area(self):
        return 3.142 * self.radius**2
        
    

class Square(Shape):
    def __init__(self,side):
        self.side = side
    
    def Area(self):
        return self.side**2
    

class Triangle(Shape):
    def __init__(self,base, height):
        self.base = base
        self.height = height
    
    def Area(self):
        return self.base * self.height * 0.5
    

class Pizza(Circle):#Now the pizza is a polyymorph because its identifies as a pizza, Circle and a shape
    def __init__(self,topping,radius):
        self.topping = topping
        super().__init__(radius)#This will call and use the radius of the Circle class
        

shapes =[Circle(4), Square(5), Triangle(6,8),Pizza("pineapple", 12)]

for shape in shapes:
    print(f"{shape.Area()} cm^2")



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#"Duck typing" = another way to achieve polymorphism besides Inheritance
#                Object must have the minimum necessary attributes/methods
#                "If it looks like a duck and quacks like a duck, it must be a duck"

class Animal:
    alive = True

class Dog(Animal):
    def Speak(self):
        print("WOOF!")

class Cat(Animal):
    def Speak(self):
        print("MEOW!")

class Car:
    #Now we have to add the alive attribute so that car can have the minimum necessary attributes/methods
    alive = False
    def Speak(self):#Though car is not a type of animal but 
        #it has the minimum necessary attributes/methods(thats "Duck typing")
        print("HONK!!")
        #Now we have to add the alive attribute so that car can have the minimum necessary attributes/methods
        

animals = [Dog(),Cat(),Car()]

for animal in  animals:
    animal.Speak()
    print(animal.alive)



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Static methods = Are methods that belong to a class rather than any object from that class (instance)
#                 usually for general utility functions

#Instance methods  = Best for operations on instances of the class (objects)
#Static methods = Best for ability function that do not need to class data

class Employee:
    
    def __init__(self,name, position):
        self.name = name
        self.position = position

    def get_info(self):#This is instance method, u have to reassign the class to access it 
        return f"{self.name} = {self.position}"
    
    @staticmethod
    def is_valid_position(position):#This s static method that can be accessed from the class directly
        valid_position = ["Manager","Cashier","Cook","janitor"]
        return position in valid_position

Employee.is_valid_position("Cashier")#This will give us "True" because Cashier is a valid position
Employee.is_valid_position("Engineer")#This will give us False

employee1 = Employee("Patrick","Janitor")
employee2 = Employee("Mr Krabs","Manager")
employee3 = Employee("SpongeBoob","Cook")

print(Employee.is_valid_position("Cashier"))
print(employee1.get_info())
print(employee2.get_info())
print(employee3.get_info())


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#Class methods = Allows Operations related to the class itself
#                Take (cls) as the first parameter, which represents the class itself


class Student:
    
    count = 0
    #to sum all the gpa
    count_gpa = 0
    
    def __init__(self, name, gpa):
        self.name = name
        self.gpa = gpa
        Student.count +=1
        Student.count_gpa += gpa
    
    #instance method 
    def get_info(self):
        return f"{self.name} {self.gpa}"
    
    @classmethod
    def get_count(cls):
        return f"Total number of student: {cls.count}"
    
    #Now to calculate the average gpa
    @classmethod
    def get_average_gpa(cls):
        if cls.count == 0:
            return 0
        else:
            return f"Class gpa average: {cls.count_gpa/cls.count}"

print(Student.get_count())#This will give us 0 for now
#Now we create students
student1 =Student("Emmanuel",4.31)
student1 =Student("Ololade",4.53)
student1 =Student("Solomon",4.02)

print(Student.get_count())#This will give us 3 now
print(Student.get_average_gpa())


#------------------------------------------------------------------------------------------------------------------------------------------------
#Magic methods = Defender methods (double underscore) __init__, __str__,__eq__
#                They are automatically called by many of the python built-in Operations.
#                They allow developers to define or customize the behavior of objects

class Book:
    def __init__(self,title,author,num_pages):#this is a magic method to enable the class to accept arguments
        self.title = title
        self.author = author
        self.num_pages = num_pages
    
    def __str__(self):#this is the string magic method use to print out the class arguments without using (book1.title/book1.author )
        return f"'{self.title}' by {self.author}"
    
    def __eq__(self, other):#magic method used to compare two objects/class
        return self.title == other.title and self.author == other.author
    
    def __lt__(self,other):#magic method used to check which object is lesser than the other based on some conditions/parameters
        return self.num_pages < other.num_pages
    
    def __gt__(self,other):#magic method used to check which object is greater than the other based on some conditions/parameters
        return self.num_pages > other.num_pages
    
    def __add__(self,other):#magic method used to add objects together based on some conditions/parameters
        return self.num_pages + other.num_pages
    
    def __contains__(self,keyword):#Magic method to check if some things are in the object
        return keyword in self.title or keyword in self.author
    
    def __getitem__(self,key):#Magic method to check for a parameter/item from an object using a keyword
        if key  == "title":
            return self.title
        elif key  == "author":
            return self.author
        elif key == "num_pages":
            return self.num_pages
        else:
            return f"{key} is not in this object"

book1 = Book("The Hobbit","J.R.R. Tolkien", 310)
book2 = Book("Harry potter the half blood prince","J.K.Rowling", 223)
book3 = Book("The Lion the witch and wardrobe","C.s. lewis", 172)

print(book1)#this will give us "<__main__.Book object at 0x0000010B1C3C92B0>" with represent the memory location of book1
#           and we need to specify what argument of parameter we want from book1 e.g book1.title/book1.author 

print(book1 == book2)#to test our __eq__ magic method
print(book1 < book2)#To test the __lt__ magic method
print(book1 > book2)#To test the __gt__ magic method
print(book1 + book2)#To test the __add__ magic method
print("Lion" in book3)#To test the __contains__ magic method
print(book1['title'])#To test the __getitem__ magic method
print(book2['author'])#To test the __getitem__ magic method
print(book2['num_pages'])#To test the __getitem__ magic method
print(book2['Color'])#To test the __getitem__ magic method incase they pass in a keys thats not in the object

