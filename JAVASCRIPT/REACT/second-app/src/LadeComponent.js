import { useContext } from "react";
import { LadeContext } from "./LadeContext";

//this component is the Ladecontext consumer
export function LadeComponent(){
 const {Data,setData}= useContext(LadeContext);
 return(
    <div>
        <h3>{Data}</h3>
        <button onClick={()=>setData('Lolade is Amazing')}>
            click
        </button>
    </div>
 )
}