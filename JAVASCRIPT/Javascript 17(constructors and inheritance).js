//CONSTRUCTORS IN JAVASCRIPT
//For example, if I want to use the pow method of the Math object to calculate exponential values, 
//there's no need to build an instance of the Math object to do so. 
//For example, to get the number 2 to the power of 5, I'd run:

Math.pow(2,5); // --> 32
//Besides constructor functions for the built-in objects, 
//I can also define custom constructor functions.
//Here's an example:
function Icecream(flavor) {
    this.flavor = flavor;
    this.meltIt = function() {
        console.log(`The ${this.flavor} icecream has melted`);
    }
}

let kiwiIcecream = new Icecream("kiwi");
let appleIcecream = new Icecream("apple");
console.log(kiwiIcecream); // --> Icecream {flavor: 'kiwi', meltIt: ƒ}
console.log(appleIcecream); // --> Icecream {flavor: 'apple', meltIt: ƒ}


//Note that using constructor functions on all built-in objects is sometimes not the best approach.
//For example, using the built-in String constructor, I can build new strings:
let apple = new String("apple");
console.log(apple); // --> String {'apple'}

//In other words, if you compare 
console.log(new String('plum') === new String('plum'))
//you'll get back false, while "plum" === "plum" returns true. 
//You're getting the false when comparing objects because 
//it is not the values that you pass to the constructor that are being compared, 
//but rather the memory location where objects are saved.


// Here's an example of using /d/ as a pattern literal:
console.log("abcd".match(/d/)); // null
console.log("abcd".match(/a/)); // ['a', index: 0, input: 'abcd', groups: undefined]

//However, when building objects of other built-in types, we can use the constructor.
//Here are a few examples:
/*new Date();
new Error();
new Map();
new Promise();
new Set();
new WeakSet();
new WeakMap();*/


//HOW INHERITANCE WORK IN JAVASCRIPT
var bird = {
    canfly: true,
    haswings: true,
    cansing: true
}
var eagle = Object.create(bird)
console.log(eagle)
console.log('Can the eagle fly: ',eagle.canfly)
console.log('does it have wings: ',eagle.haswings)
console.log('Can the bird sing: ',eagle.cansing)

var falcon = Object.create(bird)
falcon.canfly = false
console.log(falcon)
console.log('Can the eagle fly: ',falcon.canfly)//this will give you false  because of the update
console.log('does it have wings: ',falcon.haswings)
console.log('Can the bird sing: ',falcon.cansing)

class Animal {

}

class Dog extends Animal {
    constructor() {
        this.noise = "bark";
    }

    makeNoise() {
      return this.noise;
    }
}

class Wolf extends Dog {
    constructor() {
        //super();
        this.noise = "growl";
    }
}

var result = new Wolf();
console.log(result.makeNoise());