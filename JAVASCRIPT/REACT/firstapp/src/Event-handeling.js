//This part is to show how to use event handling in React
function Eventhandling(){
    const eventlistener = ()=>{
        console.log('You clicked me')
    }
    return (
        <div>
            <button onClick={eventlistener}>
                click me
            </button>
        </div>
    )
}

function Eventhandle(){
    const Hover = ()=>{
        console.log('you hovered over me')
    }
    return (
        <div>
            <button onMouseOver ={Hover}>
                hover and see
            </button>
        </div>
    )
}

function DynamicEvents(){//This component is a program that prompt users to try to guess the number the computer choses
    function handleClick() { 
        let randomNum = Math.floor(Math.random() * 3) + 1;
        //console.log(randomNum);
        let userInput = prompt('type a number');
        alert(`Computer number: ${randomNum}, Your guess: ${userInput}`);
      }
    return (
        <div>
          <h1>Task: Add a button and handle a click event</h1>
          <button onClick={handleClick}>
            Guess a number between 1 and 3
          </button>
        </div>
      );
}

export {Eventhandling, Eventhandle,DynamicEvents}