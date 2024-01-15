import {useEffect, useState} from 'react'

export function DataApp(){
 const [user2 , setuser2]  = useState([]);

 const fetchData = ()=>{
    fetch("https://randomuser.me/api/?results=1")
    .then((response) => response.json())
    .then((data) => setuser2(data));
 }
 useEffect(()=>{
    fetchData();
 },[])

 return  Object.keys(user2).length > 0 ? (
    <div>
        <h1>Data Retuned sucessfully</h1>
        <h2>Firstname is {user2.results[0].name.first}</h2>
        <h2>LastName is {user2.results[0].name.last}</h2>
    </div>
 ):(
    <h1>Data is still being fetched please be patient with us...</h1>
 )
}


//CLASS ASSIGNMENT
export function App2() {
    const [user1, setUser1] = useState([]);
  
    const fetchData = () => {
        fetch("https://randomuser.me/api/?results=1")
        .then((response) => response.json())
        .then((data) => setUser1(data));
    };
  
    useEffect(() => {
      fetchData();
    }, []);
  
    return Object.keys(user1).length > 0 ? (
      <div style={{padding: "40px"}}>
        <h1>Customer data</h1>
        <h2> Name:{user1.results[0].name.first}</h2>
        <img src={user1.results[0].picture.large} alt=""/>
  
      </div>
    ) : (
      <h1>Data pending...</h1>
    );
  }