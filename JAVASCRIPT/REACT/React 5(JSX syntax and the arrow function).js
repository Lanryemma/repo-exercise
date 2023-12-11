
function Nav(props) {
    return (
        <ul>
            <li>{props.first}</li>
        </ul>
    )
}
//Now, let's change this function declaration to a function expression:
const Nav = function(props) {
    return (
        <ul>
            <li>{props.first}</li>
        </ul>
    )
}
//Changing a component from a function declaration to a function expression doesn't 
//change its behavior, or how you write the code to render the Nav component. 
//It's still the same as they are both represented in JSX as:
/*
<Nav first="Home" />
*/


//ARROW FUNCTIONS
//Consider the Nav function expression written as an arrow function:
const Nav = (props) => {
    return (
        <ul>
            <li>{props.first}</li>
        </ul>
    )
}

//Another important rule regarding arrow functions is that using the parentheses is optional
//if there's a single parameter that a function accepts.
const Nav = props => {
    return (
        <ul>
            <li>{props.first}</li>
        </ul>
    )
}

//if your Nav component wasn't accepting any parameters, you'd code it with empty parentheses:
const Nav = () => {
    return (
        <ul>
            <li>Home</li>
        </ul>
    )
}

//Another interesting thing about arrow functions is the implicit return. However, 
//it only works if it's on the same line of code as the arrow itself. In other words, 
//the implicit return works if your entire component is a single line of code.
const Nav = () => <ul><li>Home</li></ul>

//Using Arrow Functions in Other Situations(for example, the forEach() built-in array method.)
[10, 20, 30].forEach(item => item * 10)
//You could also write this code in ES5 syntax:
[10,20,30].forEach(function(item){
    return item * 10
})



//Embedded Expressions
function namee(firtname,lastname){
 return firtname," ",lastname
}

const result=<p>{namee(Olanrewaju,Emmanuel)}</p>

//Expression in HTML attribute
//inserting a picture
const pic  = "photo.png"
const output = <img src={pic}/>