let {PI} = Math;
console.log(PI)
//now if we try to de-structure it
let {pi} = Math;
console.log(pi);//this will give you undefined as 'pi' is not recorded in the Math Object
//to compare the variable and th Math object
console.log(PI===Math.PI)//This will give me (true) as the variable 'PI' have not been updated
//Now to update the 'PI' variable 
PI = 1;
//now if we compare again
console.log(PI===Math.PI)//this will give us false


//For of loops and objects
//object is not iterable. For example:
try {
const car = {
    speed: 100,
    color: "blue"
}

for(prop of car) {
    console.log(prop)
}
}catch(err){
    console.log('THE ERROR',err)
}

//Contrary to objects, arrays are iterable. For example:  
const colors = ['red','orange','yellow']
for (var color of colors) {
    console.log(color);
}
//Luckily, you can use the fact that a for of loop can be run on arrays to loop over objects.
//But how?

//The Object.keys() method
const car2 = {
    speed: 200,
    color: "red"
}
console.log(Object.keys(car2)); // ['speed','color']
//So, when I run Object.keys() and pass it my car2 object, the returned value is an array of strings,
// where each string is a property key of the properties contained in my car2 object.


//The Object.values() method
const car3 = {
    speed: 300,
    color: "yellow"
}
console.log(Object.values(car3)); // [300, 'yellow']

//The Object.entries() method
const car4 = {
    speed: 400,
    color: 'magenta'
}
console.log(Object.entries(car4));//[ ['speed', 400], ['color', 'magenta'] ]
//This time, the values that get returned are 2-member arrays nested inside an array.



///You now have all the ingredients that you need to loop over any object's own property keys and values.
///Here's a very simple example of doing just that:
var clothingItem = {
    price: 50,
    color: 'beige',
    material: 'cotton',
    season: 'autumn'
}

for( key of Object.keys(clothingItem) ) {
    console.log(key, ":", clothingItem[key])
}

//To revisit this concept and show a practical demo of how that works, 
//let's code a function declaration that randomly assigns either
// the string speed or the string color to a variable name
function testBracketsDynamicAccess() {
    var dynamicKey;
    if(Math.random() > 0.5) {
      dynamicKey = "speed";
     }else{
       dynamicKey = "color";
     }
  
      var drone = {
        speed: 15,
        color: "orange"
      }
  
      console.log(drone[dynamicKey]);
  }
  testBracketsDynamicAccess();


  //FOR-OF-LOOP AND OBJECTS
  const car = {
    eng: true,
    steer: true,
    speed: 'slow',
  }

const sportcar = Object.create(car)
sportcar.speed = 'fast'
console.log('The sportcar Object ',sportcar)

console.log('.......for-in is unreliable..........')
for(prop in sportcar){
    console.log(prop)//+':',sportcar[prop])
}

console.log('Iterating over Object and its prototype')
console.log('......for-of is reliable.........')
for(prop of Object.keys(sportcar)){
    console.log(prop,':', sportcar[prop])
}
console.log('....it Iterates over Object own properties only...')



//THIS IS CLASS ASSIGNMENT
// Task 1
var dairy = ['cheese', 'sour cream', 'milk', 'yogurt', 'ice cream', 'milkshake']
function logDairy() {
    for (prop of dairy) {
        console.log(prop)
    }
}
//calling the function
logDairy()

// Task 2
const animal = {

canJump: true

};

const bird = Object.create(animal);

bird.canFly = true;

bird.hasFeathers = true;
//creating the function
function birdcan() {
    for (key of Object.keys(bird)) {
        console.log(key+':', bird[key])
        //console.log(`${key}: ${bird[key]}`)//this is the correct way to log it
    }
}
//calling the function
birdcan()

// Task 3
function animalCan() {
    for (keys in bird) {
        console.log(keys+':', bird[keys])
        //console.log(`${keys}: ${bird[keys]}`)//this sis the correct way to log it0
    }
}
//calling the function animalCan
animalCan()
