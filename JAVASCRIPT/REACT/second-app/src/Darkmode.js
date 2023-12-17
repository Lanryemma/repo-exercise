import { useState } from "react";

export function Darkmode(){
    const [mode , setmode] = useState([
        {backgroundColor: "grey",color: "black", border:"15px solid black",borderRadius: "8px",padding:"10px"},
        {backgroundColor: "rgb(136, 206, 45)",color: "rgb(1, 39, 8)", border:"15px solid rgb(1, 39, 8)",borderRadius: "8px",padding:"10px"},
        {backgroundColor: "gold",color: "brown", border:"15px solid brown",borderRadius: "8px",padding:"10px"}
    ])
    const change = ()=>{
        setmode([{backgroundColor: "black",color: "white", border:"15px solid grey",borderRadius: "8px",padding:"10px"},
                    {backgroundColor: "rgb(1, 39, 8)",color: "rgb(136, 206, 45)", border:"15px solid rgb(136, 206, 45)",borderRadius: "8px",padding:"10px"},
                    {backgroundColor: "brown",color: "gold", border:"15px solid gold",borderRadius: "8px",padding:"10px"}
                ])
    }
    const change2 = ()=>{
        setmode([
            {backgroundColor: "grey",color: "black", border:"15px solid black",borderRadius: "8px",padding:"10px"},
            {backgroundColor: "rgb(136, 206, 45)",color: "rgb(1, 39, 8)", border:"15px solid rgb(1, 39, 8)",borderRadius: "8px",padding:"10px"},
            {backgroundColor: "gold",color: "brown", border:"15px solid brown",borderRadius: "8px",padding:"10px"}
        ])
    }
     return(
        <div>
            <div className="first" style={mode[0]}>
                <h3>First Mode</h3>
            </div>
            <div className="second" style={mode[1]}>
                <h3>Second Mode</h3>
            </div>
            <div className="Third" style={mode[2]}>
                <h3>Third Mode</h3>
            </div>
            <button onClick={change}>
                Darkmode
            </button>
            <button onClick={change2}>
                Lightmode
            </button>
        </div>
     )
}