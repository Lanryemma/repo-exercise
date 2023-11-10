//Using array to calculate
var avg = [45,46,47,48,49,51];
var sum = 0;
//using the loop

for (i = 0;i < avg.length; i++){
    sum +=avg[i]
}
console.log(sum/avg.length)

//Using the set data structure
h1 = 'red';
h2 = 'blue';
h3 = 'red';
let house = new Set() 

house.add(h1).add(h2).add(h3)
console.log(house)//{'red','blue'}
//its gives a single red output bcoz Set() cannot repeat data

//The forEach() method
//Arrays in JavaScript come with a handy method that 
//allows you to loop over each of their members.
const fruits = ['kiwi','mango','apple','pear'];
function appendIndex(fruits, index) {
    console.log(`${index}. ${fruits}`)
}
fruits.forEach(appendIndex);
//Very often, the function that the forEach() method needs to 
//use is passed in directly into the method call, like this:
const veggies = ['onion', 'garlic', 'potato'];
veggies.forEach( function(veggie, index) {
    console.log(`${index}. ${veggie}`);
});

//The filter() method
//Another very useful method on the array is the filter() method. 
//It filters your arrays based on a specific test. 
//Those array items that pass the test are returned.
const nums = [0,10,20,30,40,50];
console.log(nums.filter( function(num) {
    return num > 20;
}))

//The map method
//This method is used to map each array item over to another array's item, 
//based on whatever work is performed inside the 
//function that is passed-in to the map as a parameter. 
console.log(nums.map( function(num) {
    return num / 10
}))


//how to work with different built-in data structures in JavaScript.
const result = [];
const drone = {
    speed: 100,
    color: 'yellow'
}
const droneKeys = Object.keys(drone);
droneKeys.forEach( function(key) {
    result.push(key, drone[key])
})
console.log(result)

//Working with Maps in JavaScript
new Map();
//A map can feel very similar to an object in JS.
//However, it doesn't have inheritance. 
//No prototypes! This makes it useful as a data storage.
//For example:
let bestBoxers = new Map();
bestBoxers.set(1, "The Champion");
bestBoxers.set(2, "The Runner-up");
bestBoxers.set(3, "The third place");

console.log(bestBoxers);
//To get a specific value, you need to use the get() method
bestBoxers.get(1); // 'The Champion'


//Working with Sets in JavaScript
//To build a new set, you can use the Set constructor:
new Set();
//The Set constructor can, for example, accept an array.
//This means that we can use it to quickly filter an array for unique members.
const repetitiveFruits = ['apple','pear','apple','pear','plum', 'apple'];
const uniqueFruits = new Set(repetitiveFruits);
console.log(uniqueFruits);

/*Some more advanced data structures that have not been covered include:

Queues

Linked lists (singly-linked and doubly-linked)

Trees

Graphs*/

function eat (...food){
    console.log(food.length)
}
eat('hoe','fish',null)