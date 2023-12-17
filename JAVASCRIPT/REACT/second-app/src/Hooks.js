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