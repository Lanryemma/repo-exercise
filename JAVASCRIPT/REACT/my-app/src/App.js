import {
  useState,
  useRef
} from "react"; 
import "./App.css";
import {DessertsList} from "./DessertsList";
import {Happ} from "./DessertsList";
import { Form } from "./Controlled/Uncontrolled form";
import { Form1 } from "./Controlled/Uncontrolled form";
import { Form2 } from "./Controlled/Uncontrolled form";
import { SignUp } from "./Sign UP Form";
import { Userprovider, useUser} from "./UserContext";

// for context example ---------------------------------------------------------------------------------
const Page =()=>{
  const {user} = useUser()
  return(
      <div>
          <div><h3>HELLO <span>{user.name}</span></h3></div>
      </div>
  )
}
const Record = ()=>{
  const {user} = useUser()
  return (
      <div>
          <p className="talk">This great book was written by the great {user.name}</p>
      </div>
  )
}

const Display =()=>{
  return(
    <div>
      <Page/>
      <Record/>
    </div>
  )
}
 const Root =()=>{
  return(
    <div>
      <Userprovider>
        <Display/>
      </Userprovider>
    </div>
  )
 }
//----------------------------------------------------------------------------------------------------



const desserts = [
  {
    name: "Chocolate Cake",
    calories: 400,
    createdAt: "2022-09-01",
  },
  {
    name: "Ice Cream",
    calories: 200,
    createdAt: "2022-01-02",
  },
  {
    name: "Tiramisu",
    calories: 300,
    createdAt: "2021-10-03",
  },
  {
    name: "Cheesecake",
    calories: 600,
    createdAt: "2022-01-04",
  },
];

function Appp() {
  return (
    <div className="App">
      <h2>List of low calorie desserts:</h2>
      <DessertsList data={desserts} />
    </div>
  )
}

function App() { 
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
        <button className="but" onClick={plus}>add</button> 
        <button className="but" onClick={minus}>subtract</button>
        <button className="but" onClick={times}>multiply</button>
        <button className="but" onClick={divide}>divide</button>
        <button className="but" onClick={resetInput}>Resetinput</button>
        <button className="but" onClick={resetResult}>Resetoutput</button>
      </form> 
      <div>
        <Appp/>
      </div>
      <div>
        <Happ/>
      </div>
      <div>
        <Form />
      </div>
      <div>
        <Form1 />
      </div>
      <div>
        <Form2 />
      </div>
      <div>
        <SignUp />
      </div>
      <div>
          <Root/>
      </div>
    </div> 
  ); 
} 

export default App;
