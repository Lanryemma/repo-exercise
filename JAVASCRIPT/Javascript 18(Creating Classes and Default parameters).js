//By now, you should know that inheritance in JavaScript is based around the prototype object.
//All objects that are built from the prototype share the same functionality.
//Take a look at this example of a Train classS
class Train {
    constructor(color, lightsOn) {
        this.color = color;
        this.lightsOn = lightsOn;
    }
}
//Now, to actually build a new instance of the Train class, I need to use the following syntax:
var myFirstTrain = new Train('red', false);
//Just like any other variable, you can now, for example, console log the myFirstTrain object:
console.log(myFirstTrain); // Train {color: 'red', lightsOn: false}
//You can continue building instances of the Train class. 
//Even if you give them exactly the same properties, they are still separate objects.
var mySecondTrain = new Train('blue', false);
var myThirdTrain = new Train('blue', false);
//You can also add methods to classes, 
//and these methods will then be shared by all future instance objects of my Train class.
class Train1 {
    constructor(color, lightsOn) {
        this.color = color;
        this.lightsOn = lightsOn;
    }
    toggleLights() {
        this.lightsOn = !this.lightsOn;
    }
    lightsStatus() {
        console.log('Lights on?', this.lightsOn);
    }
    getSelf() {
        console.log(this);
    }
    getPrototype() {
        var proto = Object.getPrototypeOf(this);
        console.log(proto);
    }
}
//hence the !this.lightsOn. And the = operator to its left 
//means that it will get assigned to this.lightsOn, 
//meaning that it will become the new value of 
//the lightsOn property on that given instance object.

//The lightsStatus() method on the Train class just reports 
//the current status of the lightsOn variable of a given object instance.

//The getSelf() method prints out the properties on the object instance it is called on.

//To get the prototype, 
//you'll be using JavaScript's built-in Object.getPrototypeOf() method

//Now you can build a brand new train using this updated Train class:
var train4 = new Train1('red', false);
//And now, you can run each of its methods, one after the other, to confirm their behavior:
console.log(train4.toggleLights()); // undefined
train4.lightsStatus(); // Lights on? true
train4.getSelf(); // Train {color: 'red', lightsOn: true}
console.log(train4.getPrototype()); // {constructor: f, toggleLights: f, ligthsStatus: f, getSelf: f, getPrototype: f}
//It is possible to implement polymorphism using classes in JavaScript, 
//by inheriting from the base class 
class HighSpeedTrain extends Train1 {
    constructor(passengers, highSpeedOn, color, lightsOn) {
        super(color, lightsOn);
        this.passengers = passengers;
        this.highSpeedOn = highSpeedOn;
    }
    toggleHighSpeed() {
        this.highSpeedOn = !this.highSpeedOn;
        console.log('High speed status:', this.highSpeedOn);
    }
    toggleLights() {
        super.toggleLights();
        super.lightsStatus();
        console.log('Lights are 100% operational.');
    }
}
var train5 = new Train1('blue', false);
var highSpeed1 = new HighSpeedTrain(200, false, 'green', false);

console.log(train5.toggleLights()); // undefined
console.log(train5.lightsStatus()); // Lights on? true
console.log(highSpeed1.toggleLights()); // Lights on? true, Lights are 100% operational.*/
//Additionally, it helps to visualize what is happening by getting 
//the prototype of both the train5 and the highSpeed1 trains:
console.log(train5.getPrototype()); // {constructor: ƒ, toggleLights: ƒ, lightsStatus: ƒ, getSelf: ƒ, getPrototype: ƒ}
console.log(highSpeed1.getPrototype()); // Train {constructor: ƒ, toggleHighSpeed: ƒ, toggleLights: ƒ}

//Using class instance as another class' constructor's property
//Consider the following example:
class StationaryBike {
    constructor(position, gears) {
        this.position = position
        this.gears = gears
    }
}

class Treadmill {
    constructor(position, modes) {
        this.position = position
        this.modes = modes
    }
}

class Gym {
    constructor(openHrs, stationaryBikePos, treadmillPos) {
        this.openHrs = openHrs
        this.stationaryBike = new StationaryBike(stationaryBikePos, 8)
        this.treadmill = new Treadmill(treadmillPos, 5)
    }
}
var boxingGym = new Gym("7-22", "right corner", "left corner")

console.log(boxingGym.openHrs) //
console.log(boxingGym.stationaryBike) //
console.log(boxingGym.treadmill) //
/*This code allows me to instantiate a new instance object of the Gym class, 
and then when I inspect it, I get the following information:

the openHrs property is equal to "7-22" (that is, 7am to 10pm)

the stationaryBike property is an object of the StationaryBike type, 
containing two properties: position and gears

the treadmill property is an object of the Treadmill type, 
containing two properties: position and modes*/

class Rectangle {
    constructor(height, width) {
      this.height = height;
      this.width = width;
    }
    // Getter
    get area() {
      return this.calcArea();
    }
    // Method
    calcArea() {
      return this.height * this.width;
    }
    *getSides() {
      yield this.height;
      yield this.width;
      yield this.height;
      yield this.width;
    }
  }
  
  const square = new Rectangle(10, 10);
  
  console.log(square.area); // 100
  console.log([...square.getSides()]); // [10, 10, 10, 10]





// I'll use an ES6 feature which allows me to 
//set a default parameter inside a function
//For example, consider a function declaration without default parameters set:
function noDefaultParams(number) {
    console.log('Result:', number * number)
}
noDefaultParams(); // Result: NaN
//the noDefaultParams its a default parameter in javascript that doesnt allow
//the function to use any of its default parameter

//Consider now, the following improvement, using default parameters:
function withDefaultParams(number = 10) {
    console.log('Result:', number * number)
}
withDefaultParams()

//This now allows me to code my classes in a way that will promote easier object instantiation.
//Consider the following class definition:
class NoDefaultParams {
    constructor(num1, num2, num3, string1, bool1) {
        this.num1 = num1;
        this.num2 = num2;
        this.num3 = num3;
        this.string1 = string1;
        this.bool1 = bool1;
    }
    calculate() {
        if(this.bool1) {
            console.log(this.string1, this.num1 + this.num2 + this.num3);
            return;
        }
        return "The value of bool1 is incorrect"
    }
}
var fail = new NoDefaultParams(1,2,3,false);
console.log(fail.calculate()); // 'The value of bool1 is incorrect'

//However, now that you know about default parameters, 
//this example can be improved as follows:
class WithDefaultParams {
    constructor(num1 = 1, num2 = 2, num3 = 3, string1 = "Result:", bool1 = true) {
        this.num1 = num1;
        this.num2 = num2;
        this.num3 = num3;
        this.string1 = string1;
        this.bool1 = bool1;
    }
    calculate() {
        if(this.bool1) {
            console.log(this.string1, this.num1 + this.num2 + this.num3);
            return;
        }
        return "The value of bool1 is incorrect"
    }
}
var better = new WithDefaultParams();
console.log(better.calculate()); // Result: 6