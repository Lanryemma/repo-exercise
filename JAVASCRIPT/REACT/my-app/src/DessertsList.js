import { useState } from "react";
function DessertsList(props) {
    // Implement the component here.
   const food = props.data.filter((result)=>{
     return result.calories < 600
   }).sort((a, b) => { 
    return a.calories - b.calories; 
  }).map((result)=> <li>{result.name} - {result.calories} cal</li>)
    return (
        <ul>{food}</ul>
    )
  }
  
  export  {DessertsList};

const Todo = (props)=>{
  return(
    <tr>
      <td>
        <label>{props.id}</label>
      </td>
      <td>
        <input/>
      </td>
      <td>
        <label>{props.createdAt}</label>
      </td>
    </tr>
  )
}

const Happ = ()=>{
  const [todos, settodos]= useState([
    {
      id:'todo1',
      createdAt: '18:00'
    },
    {
      id:'todo2',
      createdAt: '20:30'
    }
])
 const Reverseorder= ()=>{
  settodos([...todos].reverse())
 }

 return(
  <div>
    <button onClick={Reverseorder}>Reset</button>
    <table>
      <tbody>
        {todos.map((result, index)=>(<Todo key={result.id} id= {result.id} createdAt={result.createdAt}/>))}
      </tbody>
    </table>
  </div>
 )
}

export {Happ}