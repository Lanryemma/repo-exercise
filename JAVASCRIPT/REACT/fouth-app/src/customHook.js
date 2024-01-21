import { useState } from "react";
import useLadeHook from "./useLadeHook";

//This is to demonstrate how to use your own custom hook
export function CustomHook(){
    const [count, setcount]= useState(0)
    useLadeHook(count)
    
    const Increment =()=>{
        setcount(currentState => currentState + 1)//i just named it 'currenState' you can name it anything
                                                  // it represent the current value of the state
    }

    const Decrement =()=>{
        setcount(currentState => currentState - 1)//i just named it 'currenState' you can name it anything
                                                  // it represent the current value of the state
    }


    return (
        <>
            <h3>Count: {count}</h3>
            <button onClick={Increment}>
                +1
            </button>
            <button onClick={Decrement}>
                -1
            </button>
        </>
    )
}