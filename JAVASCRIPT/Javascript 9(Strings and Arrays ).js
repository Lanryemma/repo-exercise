var veg = ['carrot','lettuce','carbage','pumkin']
console.log(veg.length)
console.log(veg[0])
console.log(veg[1])

for (i = 0; i < veg.length; i++){
    console.log(veg[i])
}

console.log('')
// if you ara doing for one string
var veg1 = 'lettuce'
console.log(veg1.length)
console.log(veg1[0])
console.log(veg1[1])

for (i = 0; i < veg1.length; i++){
    console.log(veg1[i])
}
console.log('')


//though string and array have similars properties they are not the same
//and the way to prove it is using the "Array 'pop()'" function
//Here's a list of all the methods covered in this cheat sheet:
var test1 = 'carnage'
var test2 = 'venom'
for (i = 0; i < test1.length; i++){
    console.log(test1[i])
}
console.log('')

//charAt() To read each individual character at a specific index in a string,
// starting from zero, I can use the charAt() method
console.log(test1.charAt(0)); // 'c'

//concat() joins strings together
console.log("Wo".concat("rl").concat("d")); // 'World'

//indexOf()  returns the location of the first position that matches a character: 
console.log("ho-ho-ho".indexOf('-')); // 2


//lastIndexOf() finds the last match, otherwise it works the same as indexOf. 
console.log("ho-ho-ho".lastIndexOf('-')); // 5

//split() The split method chops up the string into an array of sub-strings:
console.log("hohoho".split("o")); // ['h', 'h', 'h'])

//toUpperCase() and toLowerCase() are to change from upper to lower case and viceversa
console.log(test1.toUpperCase()); // "CARNAGE, "
console.log(test2.toLowerCase()); // "venom, "


//if we console.log the pop() function for the string it will give us error
//console.log(test1.pop())//this code will give error becoz variable test1 is not an array
//console.log(test2.pop())//this code will give error becoz variable test2 is not an array

//concatination operators are used to combine strings
console.log(test1 + test2)//+ concatination Operator
console.log(test1.concat(test2))//'.concat' concatination Operator*/