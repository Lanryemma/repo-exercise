//This document deals with the creating and calling of functions
//this example shows calling normal addition calculation inside a function
function addnum (){//this is a function without parameters
    var a = 34;
    var b = 41;
    var c = a + b;
    console.log(c);
}
//now we call the function 'addnum'
addnum ();

//this example shows calling function by the value inputed in the code inside a function
function addnumber (i,j){//This is a function with parameters
    var c = i + j;
    console.log(c);
}
//now we call the function
addnumber (37,57);


//THIS PART DEALS WITH BUILDING AND STORING DATA IN AN ARRAY
//Arrays are use to group a sequence of variables (var) in a collection
//imagine two trains carrying several carriage with different materials
//instead of using console log to print everything out we can use arrays by using'[]'
var train1 = ['wheat', 'coal', 'rice', 'corn', 'wood', 'yam']
//each item in the array have been given an index number starting from '0'
//(i.e: to print rice, we know rice index number is '2' (if you are counting from '0'))
console.log(train1[2])
console.log(' ')

//This example deals with using 'array' and 'for loop' to define a function's instructions
//Since the arr.length counts the number of items in the array from one, 
//and the array items are indexed from zero, this effectively means that as soon as i is equal to arr.length,
// the loop will finish and any other code after it will be run. 
//This practically means that the exit condition for this for loop will be i < arr.length returning false. 
function listArrayItems(arr) {
    for (var i = 0; i < arr.length; i++) {
        console.log(arr[i]) //display the array item where the index is euqal to i
    }
}
//If you now invoke the listArrayItems function, I can, for example, give it the following array of colors:
var colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink'];
listArrayItems(colors); //display all items in the array at once  
console.log(' ')

//i can update the output any way I like. For example, 
//here are my arr items with a number in front of each item:
//function that takes an array as input and display all items of this array
function listArrayItem(ar) {
    for (var i = 0; i < ar.length; i++) {
        console.log(i, ar[i])
    }
}
var colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink'];
listArrayItem(colors);
console.log(' ')
//To start the count from one instead of zero, 
//I can update my function declaration as follows: 
function listArrayItemss(arrr) {
    for (var i = 0; i < arrr.length; i++) {
        console.log(i+1, arrr[i])
    }
}
var colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink'];
listArrayItemss(colors);
console.log(' ')
//I can even add one or more conditions, such as:  
//we can add an if-else statement to the function instructioins
function listArrayItemm(Arr) {
    for (var i = 0; i < Arr.length; i++) {
        if (Arr[i] == 'red') {
            console.log(i*100, "tomato!")
        } else {
            console.log(i*100, Arr[i])
        }
    }
}
var colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink'];
listArrayItemm(colors);
console.log(' ')

//THIS THE CLASS ASSIGNMENT
function letterFinder (word,match){
    for (var i = 0; i < word.length; i++){
         //this loop exists when i is equal to the length of the word
        if (word[i]==match){
            //check if the current characater, word[i], is equal to the match
            console.log('Found the', match, 'at', i)
        }else{
            console.log('---No match found at', i)
        }
    }
}
letterFinder("test", "t")

//this is example from quize.
function meal(anin){
    anin.food = anin.food + 10
}
var dog = {
    food: 10
}
meal(dog)
meal(dog)
console.log(dog.food)

console.log(' ')
//this is an exaple of using the array function for a string
function listArrayItemsQs(arrrQ) {
    for (var i = 0; i < arrrQ.length; i++) {
        console.log(i+1, arrrQ[i])
    }
}
var colorQ = 'ABCDEFG';
listArrayItemsQs(colorQ);
