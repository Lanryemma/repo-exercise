//There Are two types of programming paradigm
//functional programming paradigm and Object Oriented programming paradigm
//In functional programming, the data and functions that work on that data 
//are not combined inside objects or are seperated from the object.

//Check out this example below of functional programming
var currency1 = 100;
var currency2 = 0;
var Exchangerate = 1.5;//this are the data
function bankexchange(amount,rate){
       return amount*rate
}
currency2 = bankexchange(currency1,Exchangerate)
console.log(currency2)
//console.log(bankexchange)


//another example
//console.log('Hello');
function consoleLog(val) {
    console.log(val)
    return val
}
//now we call the function
consoleLog('Hello')

//functional programming Is useful because 
//I can use return values from one function inside another function.
//Here's an example.
//I'll first code a function that returns a double of a number that it received:
function doubleIt(num) {
    return num * 2
}
//Now I'll code another function that builds an object with a specific value:
function objectMaker(val) {
    return {
        prop: val
    }
}
//I can call the objectMaker() function with any value I like, such as:
console.log(objectMaker(20));//it will return '{prop:20}' if you run the code in the browser
//Now consider this code:
console.log(doubleIt(10).toString())

//I can even combine my custom function calls as follows:
console.log(objectMaker( doubleIt(100) ));//'{prop:200}'

//MORE EXAMPLES ON FUNCTIONAL PROGRAMMING PARADIGM
//In functional programming, we use a lot of functions and variables.
function getTotal(a,b) {
    return a + b
}
var num1 = 2;
var num2 = 3;

var total = getTotal(num1, num2);
console.log(total)
//in functional programming, functions return new values and 
//then use those values somewhere else in the code.
function getDistance(mph, h) {
    return mph * h
}
var mph = 60;
var h = 2;
var distance = getDistance(mph, h);

console.log(distance); // <====== THIS HERE!




//OBJECT ORIENTED PROGRAMMING PARADIGM
//Another style is object-oriented programming (OOP). In this style,
//we group data and functionality as properties and methods inside objects.
//For example, if I have a virtualPet object,
//I can give it a sleepy property and a nap() method:
//In OOP, methods update properties stored in the 
//object instead of generating new return values.
//creating an object
var virtualPet = {
    sleepy: true,
    nap: function() {
        this.sleepy = false
        //virtualPet.sleepy = false (you can also domit like this)
    }
}
console.log(virtualPet.sleepy) // true
virtualPet.nap()
console.log(virtualPet.sleepy) // false


/*There are many more concepts and ideas in functional programming.

 Here are some of the most important ones:

* First-class functions

* Higher-order function

* Pure functions and side-effects*/

//example of First-class functions
function addTwoNums(a, b) {
    console.log(a + b)
}

function randomNum() {
    return Math.floor((Math.random() * 10) + 1);
}
function specificNum() { return 42 };

var useRandom = true;

var getNumber;

if(useRandom) {
    getNumber = randomNum
} else {
    getNumber = specificNum
}

addTwoNums(getNumber(), getNumber())

//example of Higher-order function using the functions from the previous code above
addTwoNums(specificNum(), specificNum()); // returned number is 84
addTwoNums(specificNum(), randomNum()); // returned number is 42 + some random number

//example of Pure functions and side-effects
/*function addTwoNums(a, b) {
    console.log(a + b)
}
This function will always return the same output, based on the input. For example,
 as long as we give it a specific value, say, a 5, and a 6: 
 
 Another rule for a function to be considered pure is that it should not have side-effects.
A side-effect is any instance where a function makes a change outside of itself.

This includes: 

changing variable values outside of the function itself, or even relying on outside variables 

calling a Browser API (even the console itself!) 

calling Math.random() - since the value cannot be reliably repeated*/