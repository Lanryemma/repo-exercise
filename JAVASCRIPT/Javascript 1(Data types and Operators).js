//this is a comment
/*
this
is
a
multi-line
comment
*/
//semi colun";" is used to sepeerate a line of code from another
// and an automatic semi-colon inserter helps developers to insert the semi-colons when
//they forget to insert it
console.log("Hello World")

//If you add the %c right after the " character, you can then style the console output by adding the ','
//character after the second ", and then, inside another pair of " and " characters, 
//use valid CSS code to style the words you want to output in the console.
console.log("%cHello, World","color:blue;font-size:40px")
console.log("%cHello, World","background-color: yellow; color:blue;font-size:40px")

//To output multiple words into the console, you can join them using the + character,
 //formally known as the "concatenation operator"
 //when we're joining pieces of text, or the "addition operator", 
 //for performing the mathematical operation of adding two numbers. 
 console.log("Hello " + "there, " + "World")

 //Here is an example of outputting three separate pieces of text using the , character instead
 console.log("Hello ", "there, ", "World")

 //By using a variable, I can save a name, so that I can reuse it in the future. 
 //To save this name in a variable, I'll start with the keyword, var, 
 //and use it to signal to JavaScript that I'm giving it a value that I wanted to reuse. 
 var person = "john"
 //to use this in a greeting... we can say
 console.log("Hello", person)

 //We can also make the "hello" into a veriable too so it can also be reused or changed in the future
 var greeting = "Hello"
 //to use it in a greeting
 console.log(greeting, person)

 //We can also change the values of the variables to get differnt output
 //for example you can say - [person = "james" and greetings = "Hiii"]

 //this is class assignment on declaring variables
 var petdog = "Rex"
 var petcat = "Pepper"
 console.log(petdog)
 console.log(petcat)

 //This part is to turn it to a sentence
 console.log("My dog name is:", petdog)
 console.log("My cat name is:", petcat)

 //this is the part where we declare variables for the sounds they make
var dogsound = "woof"
var catsound = "purr"
console.log(petdog, "says", dogsound)
console.log(petcat, "says", catsound)

//Now we experiment changing the value of the 'catsound variable'
catsound = "Meow"
console.log(petcat, "now says", catsound)

//This part shows how to work with arithemethic operators
console.log(1 + 3 + 4 + 5 + 6);
console.log(3 * 17);
console.log(61 / 8);
console.log(19-4);

//This part shows the use of arithemetic operators
console.log(3 > 17);
console.log(64 < 73);
console.log(3 == 17);
console.log(3 != 17);

//This part is to show the use of strict equality and inequality
//sign which compares both values and datatype (100) is a number and
//("100") is a string meaning they are the same value but different datatypes
console.log( 100==="100")
console.log( 100!=="100")

//this  parts shows how to use the AND operator
var num = 7
console.log( num > 9 && num < 17)// this part will show false bcoz one of the statement is not true
console.log( num > 5 && num < 9)// This part will show true becoz both statement are true
console.log( num > 9 || num < 17)// this part will show true becoz atleast one of the statement(num < 17) is true

//This part shos how to use the NOT operator
var petHungry = true;

//then I can console log the fact that the pet is no longer hungry by using the ! operator 
//to flip the boolean value stored inside of the petHungry variable, like so:

console.log('Feeding the pet');
console.log("Pet is hungry: ", !petHungry);
console.log(petHungry);

//To change the value of petHungry to false permanently
petHungry = !petHungry;
console.log("The petHungry variable will now show: ", petHungry);

//This part shoe the use of the modulus Operator
console.log(22 % 5); // 2

//Combining strings and numbers using the + operator
//But what happens when one combines a string and a number using the + operator?
//Here's an example:
console.log(365 + " days") // "365 days"
console.log(12 + " months") // "12 months"
console.log(1 + "2")// "12"

//The addition assignment operator, +=
//The addition assignment operator 
//is used when one wants to accumulate the values stored in a variable.
//Here's an example: You are counting the number of overtime hours worked in a week.
var mon = 1;
var tue = 2;
var wed = 1;
var thu = 2;
var fri = 3;
console.log(mon + tue + wed + thu + fri); // 9
//You can simplify the above code by using the addition assignment operator, as follows:
var overtime = 1;
overtime += 2;
overtime += 1;
overtime += 2;
overtime += 3;
console.log(overtime); // 9

//The concatenation assignment operator, +=
//This operator's syntax is exactly the same as the addition assignment operator. 
//The difference is in the data type used:
var longString = "";
longString += "Once";
longString += " upon";
longString += " a";
longString += " time";
longString += "...";
console.log('this is what im looking for',longString); // "Once upon a time..."


//Operator precedence is a set of rules that determines which operator should be evaluated first.
//Operator associativity determines how the precedence works when the code uses operators with the same precedence.
//There are two kinds: 
//left-to-right associativity
//right-to-left associativity

//Consider the following example:
var num = 10; // the value on the right is assigned to the variable name on the left
console.log(5 > 4 > 3); // the 5 > 4 is evaluated first (to `true`), then true > 3 is evaluated to `false`, because the `true` value is coerced to `1`


//This ais the class assignment on the use of operators
var score = 8
console.log("Mid-level skills:", score > 0 && score < 10)
var timeRemaining = 0;
var energy = 10;
console.log("Game over: ", timeRemaining == 0 || energy == 0)
//to create short program that test for even number
var num1 = 2
var num2 = 5
var test1 = num1 % 2
var test2 = num2 % 2
var result1 = test1 == 0
var result2 = test2 == 0
console.log("Is", num1, "an even number?", result1)
console.log("Is", num2, "an even number?", result2)  
//this is addition operators part of the class assignment
console.log(5 + 10) 
//This part is to Concatenate numbers and strings using the + operator
var now = "Now in "
var three = 3
var d = "D!"
console.log(now + three + d)
//This part is to Use the += operator to accumulate values in a variable
var counter = 0
counter += 5
counter += 3
console.log(counter)