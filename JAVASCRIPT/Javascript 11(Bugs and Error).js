//Bug is that defect in the code that prevents it from working the way its supposed to
//when there is a bug ,the cold will still run but not give the desired result
//example of bug
function addnum(a,b){
    console.log(a+b)
}
addnum('1',2)//its gonna give us 12 but we wanted to see 3
console.log('this line still runs')//javascript printed out this line of code after skiping
//the bug in the previous line


//An error can be defined as a faulty piece of code 
//that prevents the program from further execution
//an error gets thrown and the program stops.
//common types of errors are (synthax error,type error, Range Error and reference error
//console.log(c+d);
console.log('this line wont be excuted')//this line wont run until the error of line of code above
//have been corrected

//ERROR HANDLING ('try-catch' statement.....throw keyword, you can force an error to be thrown
// from the try block to the catch block.)
try{
    console.log(c+d); 
}catch(err){
console.log(err)//.name);
//console.log(err.message);
console.log('There was a an error');
console.log('This error was saved in the error log');
}
//using the throw keyword
try{
    throw new ReferenceError();
}catch(err){
console.log(err);
console.log('There was a an error');
console.log('This error was saved in the error log');
}
console.log('This program still run');

//A RangeError is thrown when we're giving a value to a function,
// but that value is out of the allowed range of acceptable input values.
//EXAMPLE ONE 
//(Base 10 number (a number of the common decimal system) to a Base 2 number (i.e binary number))
(10).toString(2); // '1010'
// You can also use the Base 8, like this:
(10).toString(8); // 12

//However, if I try to use a non-existing number system,
// such as an imaginary Base 100, since this number system effectively doesn't exist in JavaScript
//(10).toString(100); // Uncaught RangeError: toString() radix argument must be between 2 and 36
console.log('')


//THIS IS CLASS ASSIGNMENT
function addTwoNums(a,b){
    try{
    console.log(a+b)
    }catch(err){
        console.log(err)
    }
    if (typeof(a) != 'number'){
        try{
            throw new ReferenceError();
        }catch(err){
            console.log('Error!',err)
            console.log('the first argument is not a number');
        } 
    }else if (typeof(b) != 'number'){
        try{
            throw new ReferenceError();
        }catch(err){
            console.log('Error!',err)
            console.log('the second argument is not a number');
        } 
    }else{
        console.log(a+b)
    }
}
addTwoNums(5,'5');
console.log('It still works')


//THIS IS THE RIGHT WAY TO DO IT
function addTwoNumss(c,d) {
    try {
        if(typeof(c) != 'number') {
            throw new ReferenceError('the first argument is not a number')
        } else if (typeof(d) != 'number') {
            throw new ReferenceError('the second argument is not a number')
        } else {
            console.log(c + d)
        }
    } catch(err) {
        console.log("Error!", err)
    }
}
addTwoNums(5, "5")
console.log("It still works")
console.log('')

//THIS IS THE RIGHT WAY TO DO IT
function letterFinder(word, match) {
    var condition1 = typeof(word)=='string' && word.length >= 2;
    var condition2 = typeof(match)=='string' && match.length == 1;
    if (condition1== true && condition2 ==true){
        for(i = 0; i < word.length; i++) {
            if(word[i] == match) {
                //if the current character at position i in the word is equal to the match
                console.log('Found the', match, 'at', i)
            } else {
                console.log('---No match found at', i)
            }
        }
    }else{
        console.log("Please pass correct arguments to the function.")
    }
}

//FAILING TEST TRIAL
letterFinder(23,41)

//PASSING TEST TRIAL
letterFinder('cat','t')
var result = null
console.log(result)

try{
    //throw new Error();
    console.log('Hello')
    }catch(err){
        console.log('goodbye')
    }
//throw new Error();
//console.log('hello')
try{
  Number(5).toPrecision(300)
    }catch(err){
        console.log('goodbyeee')
    }