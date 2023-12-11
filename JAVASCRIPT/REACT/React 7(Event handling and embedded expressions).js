//In this reading, you’ll learn the different ways to 
//embed expressions in event handlers in React:

/*Handling events using inline anonymous ES5 functions*/
<button onClick={function() {console.log('first example')}}>
    An inline anonymous ES5 function event handler
</button>

/*Handling events using inline anonymous ES6 functions (arrow functions)
<button onClick={() => console.log('second example')}>
    An inline anonymous ES6 function event handler
</button>*/


/*Handling events using separate function declarations*/
function App() {
    function thirdExample() {
        console.log('third example');
    };
     return (
     <div className="thirdExample">
        <button onClick={thirdExample}>
             using a separate function declaration
        </button>
     </div>
     );
};
export default App;


/*Handling events using separate function expressions*/
//A way to determine if a function is defined as an expression or 
//a declaration is: if it does not start the line with the keyword function, 
//then it’s an expression.
function Appp() {
     const fourthExample = () => console.log('fourth example');
    return (
     <div className="fourthExample">
        <button onClick={fourthExample}>
            using a separate function expression
        </button>
     </div>
     );
    };
    //export default Appp;