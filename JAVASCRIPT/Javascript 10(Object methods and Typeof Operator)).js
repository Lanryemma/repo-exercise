//Remember that all the key-value pairs in an object are referred to simply as properties.
//However, if I want to differentiate between the properties that can be executed,
//then I refer to such properties as methods. 
//take a look at the example below
//example of adding properties and methods to an object
var car = {};
car.mileage = 98765;
car.color = "red";
console.log(car);
//add a method to the car object so that it can be called as car.turnkey()
car.turnTheKey = function() {
    console.log("The engine is running")
}
//add another method to the car object so that it can be called as car.lightsOn()
car.lightsOn = function() {
    console.log("The lights are on.")
}
console.log(car);
//Remember that these method can be accessed only through the car object
car.turnTheKey();
car.lightsOn()

//NOW WE FOCUS ON THE TYPEOF OPERATOR
//the typeof operator tells you the kind of operator that is in the bracket
var test1 = typeof('ballon')
console.log(test1)

var test2 = typeof(true)
console.log(test2)

var test3 = typeof(55)
console.log(test3)

var test4 = typeof(3 < 1)
console.log(test4)

var test5 = typeof([1,2,3])
console.log(test5)

var test1 = typeof({property: 1})
console.log(test1)

var test6 = typeof(function abc(){console.log('abc')})
console.log(test6)