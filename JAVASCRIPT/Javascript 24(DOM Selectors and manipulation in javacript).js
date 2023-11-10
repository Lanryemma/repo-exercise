//JavaScript modules are standalone units of code that you can reuse again and again.
//You can think of the (DOM) Document Object model like a TV remote that lets you change the webpage content on the screen. 
//It even allows you to replace only certain parts of the page, 
//Such as an image or the heading or both 
//Example of DOM manipulation
const h2 = document.createElement('h2');
//create a new document for manupulation of the webpage
h2.innerText ='This is the heading of h2';
// I type h2.setAttribute which take in attribute name and attribute value
h2.setAttribute('id','Sub-heading');
//now we attribute a set.attribute for the class sector
h2.setAttribute('class','Secondary');
document.body.appendChild(h2)

//Javascript selector are used to manupulate the DOM in the webpage
//selectors can be used to find objects in a document
//we start by stating the document function
document
//then to access the paragraph in the webpage 
document.querySelector('p');//this will only show you the first paragraph
//then to access the anchor on the webpage
document.querySelector('a')////this will only show you the first Anchor

//now to get all all the paragraphs we use
document.querySelectorAll('p');

//to get elements on webpage based on 'id'
document.getElementById('heading')

//to get elements on webpage based on the class name
document.getElementsByClassName('txt')


//Event handling is a way of handling the website users action

const target = document.querySelector('body')

function handleClick(){
    console.log('You Clicked the body')
}

target.addEventListener('click',handleClick)

//this part is to enable clicking the header

function handleClick2(){
    console.log('You Clicked the header')
}