//Spread Operator is the shortest and simplest method to copy 
//the properties of an object onto a newly created object
//it can spread out array items and join objects together
let location = [
    'Abuja',
    'Lagos',
    'Jos'
]
 function visit(place1, place2,place3){
    console.log('First visit '+place1);
    console.log('Then visit '+place2);
    console.log('Finally visit '+place3);
 }
//to now use the spread Operator
visit(...location)


//The rest operator, on the other hand, 
//is used to build a smaller box, and pack items into it.
let locate = [
    'Abuja',
    'Lagos',
    'Jos',
    'Edo',
    'Enugu',
    'Oyo'
]
//now we use the Rest operator
//const [] = locate;
const [one,two,three,...others] = locate;
console.log(others)
//it can also be used in function
function addtax(rate,...item){
    return item.map(it => rate*it)
}
let shop = addtax(1.3,42,43,44,45,46)
console.log(shop)


//Join arrays, objects using the rest operator
//Using the spread operator, 
//it's easy to concatenate arrays:
const fruits = ['apple', 'pear', 'plum']
const berries = ['blueberry', 'strawberry']
const fruitsAndBerries = [...fruits, ...berries] // concatenate
console.log(fruitsAndBerries); // outputs a single array

//It's also easy to join objects:  
const flying = { wings: 2 }
const car = { wheels: 4 }
const flyingCar = {...flying, ...car}
console.log(flyingCar) // {wings: 2, wheels: 4}

//Add new members to arrays without using the push() method
let veggies = ['onion', 'parsley'];
veggies = [...veggies, 'carrot', 'beetroot'];
console.log(veggies);

//Convert a string to an array using the spread operator
const greeting = "Hello";
const arrayOfChars = [...greeting];
console.log(arrayOfChars); //  ['H', 'e', 'l', 'l', 'o']

//Copy either an object or an array into a separate one
const car1 = {
    speed: 200,
    color: 'yellow'
}
const car2 = {...car1}

car1.speed = 201

console.log(car1.speed, car2.speed)

//You can copy an array into a completely separate array, 
//also using the spread operator, like this:
const fruits1 = ['apples', 'pears']
const fruits2 = [...fruits1]
fruits1.pop()
console.log(fruits1, "not", fruits2)