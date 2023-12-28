import { useState } from 'react';
import { useRef } from 'react';

export function InputComponent1() { 
  const [inputText, setText] = useState('hello'); 

  function handleChange(e) { 
    setText(e.target.value); 
  } 

  return ( 
    <> 
      <input value={inputText} onChange={handleChange} /> 
      <p>You typed: {inputText}</p> 
      <button onClick={() => setText('hello')}> 
        Reset 
      </button> 
    </> 
  ); 
} 


export function TextInputWithFocusButton() {
  const inputEl = useRef(null);
  const onButtonClick = () => {
    // `current` points to the mounted text input element
    inputEl.current.focus();
  };
  let textt = "abropt";
  return (
    <>
      <input ref={inputEl} type="text" value={textt}/>
      <button onClick={onButtonClick}>Focus the input</button>
    </>
  );
}

function MyComponent() {
  const latestValue = useRef();

  const [value, setValue] = useState('');

  const handleChange = (event) => {
    setValue(event.target.value);
    latestValue.current = event.target.value;
  };

  return (
    <div>
      <input type="text" value={value} onChange={handleChange} />
      <p>Latest Value: {latestValue.current}</p>
    </div>
  );
}

export {MyComponent}


//THIS IS THE CLASS ASSIGNMENTS FOR HOOKS AND STATES
/*import {
  useState,
  useRef
} from "react"; 
import "./App.css";*/

function Assign() { 
  const inputRef = useRef(null); 
  const resultRef = useRef(null); 
  const [result, setResult] = useState(0); 
 
  function plus(e) { 
    e.preventDefault(); 
    setResult((result) => result + Number(inputRef.current.value)); 
  }; 
 
  function minus(e) { 
    e.preventDefault(); 
    setResult((result) => result - Number(inputRef.current.value)); 
  	// Add the code for the minus function 
  };
  function times(e) { 
    e.preventDefault(); 
    setResult((result) => result * Number(inputRef.current.value)); 
    // Add the code for the plus function 
  }; 
 
  function divide(e) { 
    e.preventDefault(); 
    setResult((result) => result / Number(inputRef.current.value)); 
    // Add the code for the divide function 
  };
 
  function resetInput(e) { 
    e.preventDefault(); 
    inputRef.current.value = 0;
    // Add the code for the resetInput function 
  }; 
 
  function resetResult(e) { 
    e.preventDefault(); 
    setResult(0)
  	// Add the code for the resetResult function 
  }; 
  return ( 
    <div className="App"> 
      <div> 
        <h1>Simplest Working Calculator</h1> 
      </div> 
      <form> 
        <p ref={resultRef}> 
          {result} 
        </p> 
        <input
          pattern="[0-9]" 
          ref={inputRef} 
          type="number" 
          placeholder="Type a number" 
        /> 
        <button onClick={plus}>add</button> 
        <button onClick={minus}>subtract</button>
        <button onClick={times}>multiply</button>
        <button onClick={divide}>divide</button>
        <button onClick={resetInput}>Resetinput</button>
        <button onClick={resetResult}>Resetoutput</button>
      </form> 
    </div> 
  ); 
}

export {Assign}