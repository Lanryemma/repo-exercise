import { useState } from "react";

function GoalForm(props){
 const[formData, setformData] = useState({goal:"",By: ""})

 function ChangeContent(e){
   setformData({...formData,[e.target.name]: e.target.value})
 }

 function Handlesubmit(e){
    e.preventDefault();
    props.Onadded(formData);
    setformData({goal:"",By:""})
 }

 return(
    <div>
        <h3>My 2024 Goal</h3>
        <fieldset className="goalfield">
            <form onSubmit={Handlesubmit}>
                <input type="text" name="goal" value={formData.goal} placeholder="My Goals" onChange={ChangeContent}/>
                <input type="text" name="By" value={formData.By} placeholder="By" onChange={ChangeContent}/>
                <input type="submit"/>
            </form>
        </fieldset>
    </div>
 )
}


function ListofGoal(props){
 return(
    <ul>
         {props.totalgoal.map((g)=>{
            return (<li key={g.goal}>
                <span>My goal is {g.goal} and i will achieve it by {g.By}</span>
            </li>)
         })}
    </ul>
 )
}
export function FormApp(){
    const[allgoals, setallgoals]= useState([])
    function Addgoal(goal){
        setallgoals([...allgoals,goal])
    }
    return(
        <div>
            <GoalForm Onadded = {Addgoal}/>
            <ListofGoal totalgoal={allgoals}/>
        </div>
    )
}