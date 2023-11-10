//In JavaScript, arrays are objects. 
//That means that arrays also have some built-in properties and methods.
//One of the most commonly used built-in methods on arrays are the push() and the pop() methods.
var fruits = [];
fruits.push("apple"); // ['apple']
fruits.push('pear'); // ['apple', 'pear']
//To remove the last item from an array, I can use the pop() method:  
fruits.pop();
console.log(fruits); // ['apple']
console.log(' ')

//You can now build a function that takes all its arguments and pushes them into an array, like this: 
function arrayBuilder(one, two, three) {
    var arr = [];
    arr.push(one);
    arr.push(two);
    arr.push(three);
    console.log(arr);
}
//You can now call the arrayBuilder() function, for example, like this:  
arrayBuilder('apple', 'pear', 'plum'); // ['apple', 'pear', 'plum']
console.log(' ')
//Additionally, I can save this function call to a variable. 
//I can name it anything, but this time I'll use the name
var simpleArr = arrayBuilder('apple', 'pear', 'plum');
console.log(simpleArr); // ['apple','pear','plum']
console.log(' ')

//Even better, I don't have to console log the newly built array. 
//Instead, I can return it:
function arrayBuilderr(one, two, three) {
    var ar = [];
    ar.push(one);
    ar.push(two);
    ar.push(three);
    return ar;
}
arrayBuilderr('apple', 'pear', 'plum');



//THIS IS A CLASS ASSIGNMENT FOR ARRAY AND OBJECTS
var clothes = [];
clothes.push('shirt')
clothes.push('bra')
clothes.push('shorts')
clothes.push('gown')
clothes.push('singlet')
//now we can remove the last component with 'pop()'
clothes.pop()
//we can now add a new component to the array
clothes.push('blouse')
//to show the third item in the array
console.log(clothes[2])

//This part of the assignment is for Object
var favcar = {}
favcar.color = "Blue"
favcar.convertible = true
console.log(favcar)
