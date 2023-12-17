/*Let’s say you have a component with an input text field. 
The user can type into this text field. The component needs to 
keep track of what the user types within this text field. 
You can add state and use the useState hook, to hold the string.*/
//As the user keeps typing, the local state that holds the string needs to 
//get updated with the latest text that has been typed.

//Let's discuss the below example.
import { useState } from 'react';

export function InputComponent() { 

  //The state variable "inputText" and the state function "setText" are used to 
//set the current text that is typed. The useState hook is initialized 
//at the beginning of the component 
//By default, the "inputText" will be set to “hello”.
  const [inputText, setText] = useState('hello'); 

  /*As the user types, the handleChange function, 
reads the latest input value from the browser’s input DOM element, 
and calls the setText function, to update the local state of inputText.*/
  function handleChange(e) { 
    setText(e.target.value); 
  } 

//Finally, clicking the reset button will update the inputText back to “hello”. 
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


//Hooks also come with a set of rules, that you need to follow while using them.
/*You can only call hooks at the top level of your component or your own hooks. 

  You cannot call hooks inside loops or conditions. 

  You can only call hooks from React functions, and not regular JavaScript functions. */

//To demonstrate, let’s extend the previous example, 
//to include three input text fields within a single component.
import { useState } from 'react'; 

export function RegisterForm() { 
  const [form, setForm] = useState({ 
    firstName: 'Luke', 
    lastName: 'Jones', 
    email: 'lukeJones@sculpture.com', 
  }); 

  return ( 
    <> 
      <label> 
        First name: 
        <input value={form.firstName} onChange={e => { setForm({ ...form, firstName: e.target.value }); }} /> 
      </label> 
      <label> 
        Last name: 
        <input value={form.lastName} onChange={e => { setForm({ ...form, lastName: e.target.value }); }} /> 
      </label> 
      <label> 
        Email: 
        <input value={form.email} onChange={e => { setForm({ ...form, email: e.target.value }); }} /> 
      </label> 
      <p> 
        {form.firstName}{' '} 
        {form.lastName}{' '} 
        ({form.email})
      </p> 
    </> 
  ); 
}

//In addition to the useState hook, there are other hooks that come in handy such as 
//'useContext', 'useMemo', 'useRef', etc
/*The useRef hook
We use the useRef hook to access a child element directly.

When you invoke the useRef hook, it will return a ref object. 
The ref object has a property named current*/
function TextInputWithFocusButton() {
  const inputEl = useRef(null);
  const onButtonClick = () => {
    // `current` points to the mounted text input element
    inputEl.current.focus();
  };
  return (
    <>
      <input ref={inputEl} type="text" />
      <button onClick={onButtonClick}>Focus the input</button>
    </>
  );
}