//if you have groups of data that you would like to relate, 
//you can assign them to something known as an object
//in this example imagine you are creating a game of a supermarket setting,
//each character will have to have their own traits level
//using the store manager as an example
var storemanager = {}
storemanager.strength =59;
storemanager.socialskill = 42;
storemanager.income = 100;
storemanager.activity = 'finding promotion'
//this example shows traits of a house
var house2 = {};
house2.rooms = 4;
house2.color = "pink";
house2.priceUSD = 12345;
console.log(house2); 
//To add another value to the object
house2.windows = 10;
console.log(house2); 
console.log('')
//OR U CAN ALSO CREATE OBJECT IN JAVESCRIPT LIKE THE EXAMPLE BELOW
var storeworker = {
    strength: 69,
    socialskill: 62,
    income: 50,
    activity: 'finding promotion'
} 
//another example using a table
var table = {
    legs: 3,
    color: "brown",
    priceUSD: 100,
}
console.log(table);//display the object in the developer console
//Additionally, I can console log any individual property, like this:  
console.log(table.color); // 'brown'
console.log('')
//Additionally, nothing is preventing me from combining the two approaches. For example:  
var house = {
    rooms: 3,
    color: "brown",
    priceUSD: 10000,
}
console.log(house); // {rooms: 3, color: "brown", priceUSD: 10000}
house.windows = 11;
console.log(house); // {rooms: 3, color: "brown", priceUSD: 10000, windows: 10}
console.log('')
//This flexbility additionally means that I can update already existing properties, 
//not just add new ones:
house.windows = 15;
console.log(house); // {rooms: 3, color: "brown", priceUSD: 10000, windows: 11}
console.log('')
//Object literals and the brackets notation
//This alternative syntax is known as the brackets notation.
var house3 = {};
house3["rooms"] = 4;
house3['color']= "pink";
house3["priceUSD"] = 12345;
console.log(house3); // {rooms: 4, color: 'pink', priceUSD: 12345}
console.log('')
//I can both access and update properties on objects using either the dot notation,
//or the brackets notation, or a combination of both, like in the following example:
var car = {};
car.color = "red";
car["color"] = "green";
car["speed"] = 200;
car.speed = 100;
console.log(car); // {color: "green", speed: 100}
console.log('')
//With the brackets notation, you can add to the properties
car["number of doors"] = 5;
console.log(car); // {color: 'green', speed: 100, number of doors: 5}


//consider this example
var arrOfKeys = ['speed', 'altitude', 'color'];
var drone = {
    speed: 100,
    altitude: 200,
    color: "red"
}
for (var i = 0; i < arrOfKeys.length; i++) {
    console.log(drone[arrOfKeys[i]])
}