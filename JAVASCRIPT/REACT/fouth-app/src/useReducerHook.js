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
        </div>
    )
}