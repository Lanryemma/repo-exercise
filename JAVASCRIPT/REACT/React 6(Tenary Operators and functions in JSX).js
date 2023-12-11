//A different way of writing an if...else conditional
//You are likely familiar with the structure of an if...else conditional. Here is a quick refresher:
let namee = 'Bob';
if (namee == 'Bob') {
    console.log('Hello, Bob');
} else {
    console.log('Hello, Friend');
};


//Now to write it in the ternary Operator format
//In this format the'?' is used for the if statement and
//the ':' is used for the else statement
// here's the starting if...else example, written as a ternary operator:
let nam = 'Bob';
nam == 'Bob' ? console.log('Hello, Bob') : console.log('Hello, Friend');

let condition1 = false;
let condition2 = true;
//if you are trying to write else-if in ternary
let result = condition1 ? 'Condition 1 is true': condition2 ? 'Condition 2 is true': 'Neither condition 1 nor condition 2 is true';

console.log(result);



//Using function calls in JSX
//Another way to work with an expression in JSX is to invoke a function. 

//Like the previous example, you can use function invocation inside
// JSX to return a random number:
function Example2() {
    return (
        <div className="heading">
            <h1>Here's a random number from 0 to 10: 
                { Math.round(Math.random() * 10) + 1 }
            </h1>
        </div>
    );
};

//You can also extract this functionality into a separate function:
function Example3() {

    const getRandomNum = () => Math.round(Math.random() * 10) + 1//we could use (Math.ceil/Math.floor)also

    return (
        <div className="heading">
            <h1>Here's a random number from 0 to 10: { getRandomNum() }</h1>
        </div>
    );
};

//But let’s observe both alternatives: the function expression and the function declaration.
const getRandomNum = function() {//function expression
    return Math.floor(Math.random() * 10) + 1
};

function getRandomNum() {//function declaration
    return Math.floor(Math.random() *10) + 1
};


/*--------------------------------------------------------------------------------------------*/
//Expressions as props
const bool = false;
const str1 = "just";

function Example(props) {
    return (
        <div>
            <h2>
                The value of the toggleBoolean prop is:{props.toggleBoolean.toString()}
            </h2>
            <p>The value of the math prop is: <em>{props.math}</em></p>
            <p>The value of the str prop is: <em>{props.str}</em></p>
        </div>
    );
};

export default function App() {
    return (
        <div className="App">
            <Example
                toggleBoolean={!bool}
                math={(10 + 20) / 3}
                str={str1 + ' another ' + 'string'}
            />
        </div>
    );
};
//In the example above, you’re using the !bool, that is, the NOT operator, 
//which evaluates to true, since !false is true.
//for the toggleBoolean prop to be rendered on the page, 
//you’re converting its boolean value to a string using  JavaScript’s built-in .tostring method

//The math prop is there to show that you can 
//add arithmetic operators and numbers inside JSX

//The str prop is there to show that you can concatenate strings