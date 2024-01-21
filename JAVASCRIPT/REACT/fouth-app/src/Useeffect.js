import {useEffect, useState} from "react"

export function EffectApp(){
    const [toggle,settoggle]= useState(false)
     const Changetoggle = ()=>{
        settoggle(!toggle)
     }
     //Use the useEffect to change the document title
     useEffect(()=>{
        document.title = toggle ? "This is the initial state":"A change has occured"
        //if u want irt to only change when the app is launched
        //We will use the Array Dependency '[]' 
     }, [toggle])
     //if we want the useEffect to render based on a state we place the state or function
     //in the dependency array (e.g the 'toggle' state)
    return(
        <div>
            <h2>Using the useEffect for the toggle message</h2>
            <button onClick={Changetoggle}>
                view
            </button>
            {toggle && <p>This Message will Disappear when you click again</p>}
        </div>
    )
 }