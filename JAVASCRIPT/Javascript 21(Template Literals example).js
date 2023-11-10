//Differences between a template and regular string
//First, it allows for variable interpolation:
let greet = "Hello";
let place = "World";
console.log(`${greet} ${place} !`) //display both variables using template literals
//Essentially, using template literals allows programmers to embed variables directly in between the backticks,
//without the need to use the + operator and the single or double quotes
//In other words, in ES5, the above example would have to be written as follows:  
/*var great = "Hello";
var place = "World";*/
console.log("string text line 1\n" + "string text line 2");
// "string text line 1
// string text line 2"
console.log(greet + " " + place + "!"); //display both variables without using template literals
//Besides variable interpolation, template strings can span multiple lines.
//For example, this is perfectly good syntax:
console.log(`Hello,
World
!
`)
//Notice that this can't be done using string literals
/*"Hello,
World"*/
////it's possible to perform arithmetic operation inside a template literal expression
console.log(`${1 + 1 + 1 + 1 + 1} stars!`) 


//USING ES6 template literals
let multiline = `
john
marry
samson
david
bryan
`
console.log(multiline)

//Es6 variable interpolation
let first = `How much do you know ? `
let second = `would you like to learn more`
console.log(`${first},This is a question that needs a quick response,${second}`)
