//it involves using objects to group related data and functionality
//this exampe is to calculate the total price of a shoe
var buy = {
    shoe: 100,
    taxrate: 1.2,
    totalamount: function(){
        var calculate = buy.shoe*buy.taxrate;
        console.log('The total price is: ',calculate)
    }
}
//caling the function in the object
buy.totalamount()

//you can improve the code by using the 'this' keyword
var buyy = {
    shoe: 150,
    taxrate: 1.2,
    totalamoun: function(){
        var calculate = this.shoe*this.taxrate;
        console.log('The total price is: ',calculate)
    }
}
//caling the function in the object
buyy.totalamoun()

//IF YOU ARE USING FUNCTIONAL PROGRAMING PARADIGM
var shoe = 139;
var taxrate = 1.5;
function total(){
    var cal = shoe*taxrate;
    return cal
}
console.log('The price is meant to be: ',total())



//CLASSES IN OBJECT ORIENTED PROGRAMMING 
//To code this efficiently, you can use something called classes.
//They are essentially a blueprint that you can repeatedly use to build new objects of a certain kind,
//as many times as you like.
//OOP also:
//Allows you to write modular code,
//Makes your code more flexible and
//Makes your code reusable.
//The four fundamental OOP principles are 
//inheritance, encapsulation, abstraction and polymorphism
//utilize the Object.create() method. to create or instansiate objects of our classes
class Animal { /* ...class code here... */ }
var myDog = Object.create(Animal)
console.log (Animal)
//A more common method of creating obbjects from classes is to use the new  keyword
class animal { /* ...class code here... */ }
var myDog = new animal()
console.log (animal)

//OOP Principles: Inheritance
//Note that each sub-class inherits from its super-class. 
//In turn, a sub-class might also be a super-class, 
//if there are classes inheriting from that sub-class.
//To setup the inheritance relation between classes in JavaScript, 
//I can use the extends keyword, as in class B extends A.
class Animall { /* ...class code here... */ }
class Bird extends Animall { /* ...class code here... */ }
class Eagle extends Bird { /* ...class code here... */ }


//OOP Principles: Encapsulation
//In the simplest terms, encapsulation has to do with making a code 
//implementation "hidden" from other users, 
//in the sense that they don't have to know how my code works in order to "consume" the code.


//OOP Principles: Abstraction
//Abstraction is all about writing code in a way that will make it more generalized.
//An abstraction is about extracting the concept of what you're trying to do, 
//rather than dealing with a specific manifestation of that concept. 


//OOP Principles: Polymorphism
//Polymorphism is a word derived from the Greek language meaning "multiple forms". 
//An alternative translation might be: "something that can take on many shapes".
//imagine a door bell and a bicycle bell, they both bells but one is to bring someone 
//to answer the door and the other is to alert people to clear the road
const bicycle = {
    bell: function() {
        return "Ring, ring! Watch out, please!"
    }
}
const door = {
    bell: function() {
        return "Ring, ring! Come here, please!"
    }
}
console.log(bicycle.bell()); // "Get away, please"
console.log(door.bell()); // "Come here, please"
//Now, to make this code truly polymorphic, 
//I will add another function declaration:
function ringTheBell(thing) {
    console.log(thing.bell())
}
//now to call the function
ringTheBell(bicycle); // Ring, ring! Watch out, please!
ringTheBell(door); // "Ring, ring! Come here, please!"

//Here's another example,the concatenation operator, 
//used by calling the built-in concat() method
console.log("abc".concat("def")); // 'abcdef'
console.log(["abc"].concat(["def"])); // ['abc', 'def']
//Consider using the + operator on two arrays with one member each: 
console.log(["abc"] + ["def"]); // ["abcdef"] 
//This means that the concat() method is exhibiting polymorphic behavior 
//since it behaves differently based on the context - in this case, 
//based on what data types I give it


//Here's an example of polymorphism using classes in JavaScript:
class bird {
    useWings() {
        console.log("Flying!")
    }
}
class eagle extends bird {
    useWings() {
        super.useWings()
        console.log("Barely flapping!")
    }
}
class Penguin extends bird {
    useWings() {
        console.log("Diving!")
    }
}
var baldEagle = new eagle();
var kingPenguin = new Penguin();
baldEagle.useWings(); // "Flying! Barely flapping!"
kingPenguin.useWings(); // "Diving!"

//this part invoves creating example of class with dog example
class caniane {
    dogs(){
        console.log('bark like a')
    }
}
class bulldog extends caniane{
    dogs(){
        super.dogs()
        console.log('Bull Dog')
    }
}
class chiwawa extends caniane{
    dogs(){
        super.dogs()
        console.log('Chiwawa Dog')
    }
}
var bdog = new bulldog();
var cdog = new chiwawa();
bdog.dogs();
cdog.dogs();