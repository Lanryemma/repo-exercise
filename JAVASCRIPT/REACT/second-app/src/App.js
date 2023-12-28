import logo from './logo.svg';
import './App.css';
import Intro1 from './Intro1';
import Intro2 from './Intro2';
import Intro3 from './Intro3';
import Nav from './Nav';
import Promo from './Promo';
import Footer from './Footer';
import { InputComponent1, TextInputWithFocusButton } from './Hooks';
import { Change1, Repeat } from './State';
import { useState } from 'react';
import {LadeComponent} from './LadeComponent'
import { LadeContext } from './LadeContext';
import Fruits from "./Fruits";
import FruitsCounter from "./FruitsCounter";
import { Darkmode } from './Darkmode';
import Sharing from './Sharing'
import { Assign } from './Hooks';



//This class assignment
function AApp() {
  const [fruits] = useState([
       {fruitName: 'apple', id: 1},
       {fruitName: 'apple', id: 2},
       {fruitName: 'plum', id: 3},
   ]);
 return (
   <div className="App">
     <h1>Where should the state go?</h1>
     <Fruits state = {fruits} />
     <FruitsCounter state = {fruits} />
   </div>
 );
}



//This is to demonstrate how to use context API
function Context(){
  const [Data, setData] = useState('')
  //now we will use the provider function
  return(
    <div>
      <LadeContext.Provider value={{Data,setData}}>
        <LadeComponent/>
      </LadeContext.Provider>
    </div>
  )
}

//we are also going to try and demostrate how props work
function App() {
  const introstyle = {
    margin: "10px 10px",
    fontStyle: "italic",
    backgroundColor: "rgb(197, 12, 197)",
    borderRadius: "8px",
  }
  return (
    <div className="App">
      <div>
        <Nav name="EMMANUEL" Color="YELLOW"/>
      </div>
      <div>
        <Promo product="Falafel"/>
      </div>
      <div className="in1" style={introstyle}>
        <Intro1 News="Great News"/>
      </div>
      <div>
        <Intro2/>
      </div>
      <div>
        <Intro3/>
      </div>
      <div>
        <Footer/>
      </div>
      <div>
        <InputComponent1/>
      </div>
      <div>
        < TextInputWithFocusButton/>
      </div>
      <div>
        <Change1/>
        <Repeat/>
      </div>
      <div>
        <Context/>
      </div>
      <div>
        <AApp/>
      </div>
      <div>
        <Darkmode/>
      </div>
      <div>
        <Sharing/>
      </div>
      <div>
        <Assign/>
      </div>
    </div>
  );
}

export default App;
