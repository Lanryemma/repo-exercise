import { useReducer } from "react";

const Reducer = (state,action)=>{
    if(action.type === "Buy-ingridient")return {money: state.money-10}
    if(action.type === "sell-to-customer")return {money: state.money+10}
    if(action.type === "Celebrity-Visited")return {money: state.money+1000}
    return state
}


export const ReducerApp = ()=>{
    const statedefine = {money: 100}
    const[state, dispatch]= useReducer(Reducer, statedefine)

    return (
        <div className="Reducer">
            <h3> Wallet Balance: {state.money}$</h3>
            <button onClick={()=> dispatch({type:"Buy-ingridient"})}>Shoping for veggies</button>
            <button onClick={()=> dispatch({type:"sell-to-customer"})}>Serving customer meal</button>
            <button onClick={()=> dispatch({type:"Celebrity-Visited"})}>Celebrity-Visited</button>
            <Form/>
        </div>
    )
}


//import { useReducer } from 'react';

function reducer(state, action) {
  switch (action.type) {
    case 'incremented_age': {
      return {
        name: state.name,
        age: state.age + 1
      };
    }
    case 'changed_name': {
      return {
        name: action.nextName,
        age: state.age
      };
    }
  }
  throw Error('Unknown action: ' + action.type);
}

const initialState = { name: 'Taylor', age: 42 };

 function Form() {
  const [state, dispatch] = useReducer(reducer, initialState);

  function handleButtonClick() {
    dispatch({ type: 'incremented_age' });
  }

  function handleInputChange(e) {
    dispatch({
      type: 'changed_name',
      nextName: e.target.value
    }); 
  }

  return (
    <>
      <input
        value={state.name}
        onChange={handleInputChange}
      />
      <button onClick={handleButtonClick}>
        Increment age
      </button>
      <p>Hello, {state.name}. You are {state.age}.</p>
    </>
  );
}
