//Web page content update
//In this reading, you will learn how to capture user input and process it
//to demonstrate how to manipulate information displayed based on user input.
//To capture user input, you can use the built-in prompt() method
let ans = prompt('What is your name?');
//you can output the typed-in information on the screen, as an <h1> HTML element
let answer = prompt('What is your name?');
if (typeof(answer) === 'string') {
    var h1 = document.createElement('h1')
    h1.innerText = answer;
    document.body.innerText = '';
    document.body.appendChild(h1);
}

//You can code a script which will take an input from an HTML form and 
//display the text that a user types in on the screen.
var h1 = document.createElement('h1')
h1.innerText = "Type into the input to make this text change"

var input = document.createElement('input')
input.setAttribute('type', 'text')

document.body.innerText = '';
document.body.appendChild(h1);
document.body.appendChild(input);

//now to set up an event listener
//In this case, the change event will fire after you've 
//typed into the input and pressed the ENTER key.
var h1 = document.createElement('h1')
h1.innerText = "Type into the input to make this text change"

var input = document.createElement('input')
input.setAttribute('type', 'text')

document.body.innerText = '';
document.body.appendChild(h1);
document.body.appendChild(input);

input.addEventListener('change', function() {
    console.log(input.value)
})

//Now to update the text content of the h1 element 
//with the value you got from the input field.
var h1 = document.createElement('h1')
h1.innerText = "Type into the input to make this text change"

var input = document.createElement('input')
input.setAttribute('type', 'text')

document.body.innerText = '';
document.body.appendChild(h1);
document.body.appendChild(input);

input.addEventListener('change', function() {
    h1.innerText = input.value
})


//class assignment
var h1 = document.querySelector('h1')
var arr = ['Example Domain','First Click','Second Click','Third Click'];
function handleClick(){
    switch(h1.innerText){
        case arr[0]:
            h1.innerText = arr[1];
            break;
        case arr[1]:
            h1.innerText = arr[2];
            break;
        case arr[2]:
            h1.innerText = arr[3];
            break;
        default:
            h1.innerText = arr[0];

    }
}
h1.addEventListener('click',handleClick)