//UNCONTROLLED COMPONENTS
//Form data is handled by the DOM itself
const Form = () => { 
    const inputRef = useRef(null); 
   
    const handleSubmit = () => { 
      const inputValue = inputRef.current.value; 
      // Do something with the value 
    } 
    return ( 
      <form onSubmit={handleSubmit}> 
        <input ref={inputRef} type="text" /> 
      </form> 
    ); 
}; 


//CONTROLLED COMPONENTS
//Controlled inputs accept their current value as a prop and a callback to change that value.
//Form data is handled by the component state
const Form2 = () => { 
    const [value, setValue] = useState(""); 
   
    const handleChange = (e) => { 
      setValue(e.target.value) 
    } 
   
    return ( 
      <form> 
        <input 
          value={value} 
          onChange={handleChange} 
          type="text" 
        /> 
      </form> 
    ); 
}; 



//There are some specific form inputs that are always uncontrolled, like the file input tag. 
//in React,an <input type="file" /> is always an uncontrolled component because its value
//is read-only and can't be set programmatically. 

//an <input type="file" /> is always an uncontrolled component because 
//its value is read-only and can't be set programmatically. 
const Form3 = () => { 
    const fileInput = useRef(null); 
   
    const handleSubmit = (e) => { 
      e.preventDefault(); 
      const files = fileInput.current.files; 
      // Do something with the files here 
    } 
   
    return ( 
      <form onSubmit={handleSubmit}> 
        <input 
          ref={fileInput} 
          type="file" 
        /> 
      </form> 
    ); 
   
};


/*Conclusion 

Uncontrolled components with refs are fine if your form is incredibly simple regarding UI feedback. 
However, controlled input fields are the way to go if you need more features in your forms. 
Evaluate your specific situation and pick the option that works best for you.
The below table summarizes the features that each one supports:

FEATURE DIFFERENCES
=================================================================
One-time value retrieval (e.g. on submit)

Yes - Uncontrolled

Yes - Controlled
--------------------------------------------------------------------
Validating on submit

Yes - Uncontrolled

Yes - Controlled
----------------------------------------------------------------------
Instant field validation

No - Uncontrolled

Yes - Controlled
--------------------------------------------------------------------
Conditionally disabling a submit button

No - Uncontrolled

Yes - Controlled
----------------------------------------------------------------------
Enforcing a specific input format

No - Uncontrolled

Yes - Controlled
-----------------------------------------------------------------------
Several inputs for one piece of data

No - Uncontrolled

Yes - Controlled
---------------------------------------------------------------------------
Dynamic inputs

No - Uncontrolled

Yes - Controlled
*/