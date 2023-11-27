//this is to refresh my memories on some javascript concepts

const { Children } = require("react");

//alert('hello world');
console.error('This is an error');
console.warn('This is a warning');

//testing for data types
const name = 'john';
const age =30;
const score = 40.5;
const display = null;
const notdefined = undefined;
const boolean = true;
let F;
//now we test the type of data type
console.log(typeof display)
console.log(typeof F)

//concatinating with template literals
console.log(`my name is ${name} and i am ${age} years old`)
//We can assign it to a const
const about = `my name is ${name} and i am ${age} years old`
console.log(about)
//----------------------------------------------------------------------------

//This is part deals with with string properties and methods
const word = 'Hello World!'
console.log(word.length)//gives the length of the word
console.log(word.toUpperCase())
console.log('')//this is to create space

//we can use the substring method to get the letters by index numbers
console.log(word.substring(0,5));//u can also do it to uppercase
console.log(word.substring(0,5).toUpperCase());

//using the split method
console.log(word.split(''))
console.log('')

//trying to capitalize the first letter
const capital = word.split('')
const result = capital[0].toLowerCase() + word.slice(1)
console.log(result)
console.log('')

//This is using chatgpt method
const word2 = 'hello world!';
const capitalizedWord = word2.charAt(0).toUpperCase() + word2.slice(1);

console.log(capitalizedWord);  // Output: Hello world!
//----------------------------------------------------------------------------------------


//THIS PART IS FOR ARRAY
const array = ['boy','girl','animal', 10,23,12]
console.log(array)
//to pick a particular element in the array
console.log(array[3])

//to add elements to the array
array[6]= 'ball'
console.log(array)
console.log('')
//or we can use the push method which is useful when u domt know howmany elements are in te array
array.push(567)
console.log(array)
console.log('')
//if we want tomadd the element to the beginning of the array
array.unshift('infront')
console.log(array)
console.log('')
//to remove the last elements from the array
array.pop()
console.log(array)
console.log('')
//to check if the variable is an array
console.log(Array.isArray(array))//true
console.log(Array.isArray(word))//false
//to get the index of an array element
console.log(array.indexOf('animal'))//we get'3'
//--------------------------------------------------------------------------------


//THIS PART IS FOR OBJECTS
const object = {
    firstname: 'Daniel',
    Lastname: 'Little',
    Age: 34,
    //Now we dempnstrate how we can add an array in a object
    Hobbies: ['Jumping','Dancing','Acting'],
    //Now we put an object within an object
    Address: {
        State: 'Lagos',
        city: 'Ikotun',
        Street: 'Obadore'
    }
}
//now we print it out
console.log(object.firstname, object.Lastname)
console.log('')
//to print from the array
console.log(object.Hobbies[2])//Acting
console.log('')
//to print for objects in object
console.log(object.Address.city)//ikotun

//nw we can pull things out
const {firstname,Lastname, Address:{city}} = object
console.log(Lastname)//this gives 'Little'
console.log(city)//ikotun
console.log('')

//you can also add things to the object
object.car = 'Camry';
console.log(object)
console.log('')

//In javascript we work with array that has objects as its elements
const todos = [
    {
        task: 1,
        activity:'take out the trash',
        completed: true 
    }
,
    {
        task: 2,
        activity:'take my bath and get ready',
        completed: true
    }
,
    {
        task: 3,
        activity:'Have meeting with the boss',
        completed: false,
    }
]
console.log(todos)
//to print out elements from each object in the array
console.log(todos[1].activity)
console.log('')

//Now we show how to convert our array to JSON file incase we want to send it to the server
const todolist = JSON.stringify(todos);

console.log(todolist)
console.log('')
//-------------------------------------------------------------------------------------------------------


//THIS PART IS FOR LOOPS
for(let b = 0; b < 11; b++){//for loop
    console.log(`For loop number: ${b}`)
}
//while loop
console.log('')

let a = 0;
while(a<6){
    console.log(`While loop number: ${a}`)
    a++
}
console.log('')
//you can loop through the array
for(let r =0; r< todos.length; r++){
    console.log(todos[r].activity)
}
//we can use the of loop method
for( let loop of todos){//'loop' is just a word i used it can be anything
    console.log(loop.task)
}
console.log('')

//HIGH ORDER ARRAY METHODS ARE THE PROPER WAY TO LOOP THROUGH ARRAY
//it includes 'filters','maps' and 'forEach'
todos.forEach(function(avalue){//we use a function parameter to asign the new value'avalue'
    console.log(avalue.completed)
})//foreach
console.log('')

//MAP
const maptodos = todos.map(function(value2){//Map creates an array from an existing array document
    return value2.activity
})
console.log(maptodos)
console.log('')

//filters
const filtertodos = todos.filter(function(value3){//we will get only the part of the array where completed = true
    return value3.completed === true
})
console.log(filtertodos)
console.log('')

//Now we combined two of the methods together
const combine = todos.filter((value4)=>{
    return value4.task > 1
}).map(function(value4){
    return value4.completed
})
console.log(combine)
console.log('')
//----------------------------------------------------------------------------------------------------------------------------


//TERNARY CONDITIONAL STATEMENT'?'
var x = 10;
//now we use ternary conditional statement'?'
//in the statement below , if x > 10 then color = blue (else = ':') color = yellow
const color = x > 10 ? 'blue' : 'yellow'
console.log(color)
console.log('')
//-----------------------------------------------------------------------------------------------------------------------------

//Arrow Function
const addnum = (num1, num2)=>{
    return num1 + num2;
}
console.log(addnum(34,71))

//we could write it like this
const add = (num1,num2)=> num1 + num2;
console.log(add(23,47))
console.log('')
//-------------------------------------------------------------------------------------------------------------------------------


//Object oriented programming
//constructor functions
function Info(Firstname,lastname,dob){
    this.Firstname = Firstname;
    this.lastname = lastname;
    this.dob = new Date(dob);
    this.getbirthyear = function(){//this is called a method
        return this.dob.getFullYear();
    }
    /*this.getfullname = function(){
        return `${Firstname} ${lastname}`
    }*/
}

let Person1 = new Info('Ololade','Emmanuel','12-07-2000')
let Person2 = new Info('kelvin','Olanrewaju','11-08-2010')
console.log(Person1)

console.log(Person2.lastname)

console.log(Person1.getbirthyear())
//console.log(Person1.getfullname())
console.log('')

//A better method to write this is with prototyping
Info.prototype.getFullname1 = function(){
    return`  ${this.Firstname} ${this.lastname}`
}

Info.prototype.getBirthyear = function(){//this is called a method
    return this.dob.getFullYear();
}
console.log(Person1.getBirthyear())
console.log(Person2.getFullname1())

//ANOTHER BETTER WAY OF WRITING CONSTRUTOR FUNCTION IS USING CLASSES
class classperson {
    constructor(Firstname,lastname,dob){
    this.Firstname = Firstname;
    this.lastname = lastname;
    this.dob = new Date(dob);
    this.getbirtyear = function(){//this is called a method
        return this.dob.getFullYear();
    }
}  
}

classperson.prototype.getfulname = function(){
    return `${this.Firstname} ${this.lastname}`
}

let Person3 = new classperson('Ololade','Emmanuel','12-07-2000')
console.log(Person3.getbirtyear())
console.log(Person3.getfulname())
console.log('')
//--------------------------------------------------------------------------------------------------------------------------------------




//THIS PART DEALS WITH DOM SELECTION
//SINGLE ELEMENT SELECTORS
//console.log(window)//Test it on the browser developertool to see effect

//select element by id
document.getElementById('form-id')
console.log(document.getElementById('form-id'))//Test it on the browser developertool to see output

//this one selects any single elements by query
document.querySelector('h3')//it will only select the first h3
document.querySelector('.container')//it can also select class
document.querySelector('#form-id')//it can also select id too
console.log(document.querySelector('#form-id'))

//Multiple element
//we use this to select multiple items
console.log(document.querySelectorAll('.item'))

//we can also get multiple of one element
console.log(document.getElementsByClassName('item'))
console.log(document.getElementsByTagName('form'))

//NOW WE TRY TO LOOP THROUGH THE LIST like an array
const items = document.querySelectorAll('.item');


for (let it = 0; it< items.length; it++){
    console.log(items[it])
}

//it can also be done this way
items.forEach((loopover)=> console.log(loopover))
//-----------------------------------------------------------------------------------------------------------------


//WE MOVE TO MANIPULATING DATA IN THE DOM
const ul = document.querySelector('.item')
//ul.remove();//this will remove anything with the class 'item'

//ul.lastElementChild.remove()//remove the last element with the class 'item'
//ul.firstElementChild.remove()//remove the first element with the class 'item'

//ul.children[3].innerText= 'blood';//the change the text of the fouth element to 'blood
//ul.children[1].textContent = 'content 2';//the change the text of the second element to 'content 2'
ul.children[1].innerHTML = 'content two';//the change the text of the second element to 'content 2'

ul.children[1].innerHTML = '<h1>LIST HEADING</h1>'//this will add heading one to the sencond element

//Using javascript toaffect the style of the DOM
const clor = document.querySelector('.btn')

clor.style.background = 'red'//this is used to change the color of the submit button to red
//----------------------------------------------------------------------------------------------------------------------------------


//NOW WE USE EVENT LISTENER
//we give the submit button an Event and a function to  do
const lor = document.querySelector('.btn')
lor.style.background = 'red'
lor.addEventListener('click',function(e){
    e.preventDefault();//This removes the default submit button function which is to submit the form
    //console.log('clicked')//it logs'clicked' anytime you click
    //console.log(e.target)//this is to print the main element using the event
    //document.querySelector('#form-id').style.background = 'gold'//this change the background color of the form when clicked
    document.querySelector('.container').style.background = 'aqua'//this change the background color of the container when clicked
})