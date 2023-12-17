//State is componnet internal Data that determine the current
//behaviour of the component..State are kept in form of variables
import React, {useState} from 'react'
export function Change (){
 const [Word , setWord] = useState('Eat')
 let condition = true;
 function Set (){
    condition =!condition
    if(condition === true){
        setWord('Eat')
    }else if(condition === false){
        setWord('Drink')
    }
 }
  return (
    <div>
        <h3>You can {Word} well at little Lemon Restaurant</h3>
        <button onClick={Set}>
            change
        </button>
    </div>
  )
}
/*============================================================================================================*/



//PROP DRILLING
function Main(props) { 
    return <Header msg={props.msg} />; 
  };
  
  function Header(props) { 
    return ( 
      <div style={{ border: "10px solid whitesmoke" }}> 
        <h1>Header here</h1> 
        <Wrapper msg={props.msg} /> 
      </div> 
    ); 
  };
  
  function Wrapper(props) { 
    return ( 
      <div style={{ border: "10px solid lightgray" }}> 
        <h2>Wrapper here</h2> 
        <Button msg={props.msg} /> 
      </div> 
    ); 
  };
  function Button(props) { 
    return ( 
      <div style={{ border: "20px solid orange" }}> 
        <h3>This is the Button component</h3> 
        <button onClick={() => alert(props.msg)}>Click me!</button> 
      </div> 
    ); 
  };
  
  function App() { 
    return ( 
      <Main  
        msg="I passed through the Header and the Wrapper and I reached the Button component"  
      /> 
    ); 
  }; 
  
  export default App;
/*=========================================================================================================*/


//USING CONTEXT API TO MANAGE STATE
