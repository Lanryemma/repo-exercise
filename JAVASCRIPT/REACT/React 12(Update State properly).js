//The correct way to update the state object in React when using useState
//The suggested approach for updating the state object in React 
//when using useState is to copy the state object and then update the copy.
//This usually involves using the spread operator (...).

import { useState } from "react"; 
 
export  function App() { 
  const [greeting, setGreeting] = useState({ greet: "Hello, World" }); 
  console.log(greeting, setGreeting); 
 
  function updateGreeting() { 
    const newGreeting = {...greeting}; 
    newGreeting.greet = "Hello, World-Wide Web"; 
    setGreeting(newGreeting); 
  } 
 
  return ( 
    <div> 
      <h1>{greeting.greet}</h1> 
      <button onClick={updateGreeting}>Update greeting</button> 
    </div> 
  ); 
} 


//Updating the state object using arrow functions
//Now, let’s use a more complex object to update state.
export function App1() { 
    const [greeting1, setGreeting1] = useState( 
      { 
          greet: "Hello", 
          place: "World" 
      } 
    ); 
    console.log(greeting1, setGreeting1); 
   
    function updateGreeting1() { 
      setGreeting1(prevState => { 
          return {...prevState, place: "World-Wide Web"} 
      }); 
    } 
   
    return ( 
      <div> 
        <h1>{greeting1.greet}, {greeting1.place}</h1> 
        <button onClick={updateGreeting1}>Update greeting</button> 
      </div> 
    ); 
  } 
