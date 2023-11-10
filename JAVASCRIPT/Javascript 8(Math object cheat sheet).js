/*Number constants
Here are some of the built-in number constants that exist on the Math object: 

The PI number: Math.PI which is approximately 3.14159

The Euler's constant: Math.E which is approximately 2.718

The natural logarithm of 2: Math.LN2 which is approximately 0.693*/


/*Rounding methods
These include: 

 Math.ceil() - rounds up to the closest integer 

 Math.floor() - rounds down to the closest integer 

 Math.round() - rounds up to the closest integer if the decimal is .5 or above; otherwise, rounds down to the closest integer 

 Math.trunc() - trims the decimal, leaving only the integer*/


/*Arithmetic and calculus methods
Here is a non-conclusive list of some common arithmetic and calculus methods that exist on the Math object: 

Math.pow(2,3) - calculates the number 2 to the power of 3, the result is 8 

Math.sqrt(16) - calculates the square root of 16, the result is 4 

Math.cbrt(8) - finds the cube root of 8, the result is 2 

Math.abs(-10) - returns the absolute value, the result is 10 

Logarithmic methods: Math.log(), Math.log2(), Math.log10() 

Return the minimum and maximum values of all the inputs: Math.min(9,8,7) returns 7, Math.max(9,8,7) returns 9.

 Trigonometric methods: Math.sin(), Math.cos(), Math.tan(), etc.*/

//Take a look at the example
//using Math.random() to generate random numbers between 0 and 0.99
Math.random();
//save it to a variable 
var decimal = Math.random();
// log the output of the decimal variable
console.log(decimal)
//at default math.random generate random value from 0-0.99
//to get it to generate random value that range from 0 - 10, you multiply buy '10' or '20'(from 0 - 20) e.t.c
console.log(decimal*10)
console.log(decimal*20)
console.log(decimal*30)

//Math.ceil() - rounds up to the closest integer 
//this is an example
var rounded = Math.ceil(0.009);
var rounde = Math.ceil(0.5);
console.log(rounded)
console.log(rounde)

var round = Math.ceil(1.5);
var roun = Math.ceil(2.05);
console.log(round)
console.log(roun)


//We can combine both of this maths Objects
var num = Math.random()*10;
var num2 = Math.ceil(num)
console.log(num2)