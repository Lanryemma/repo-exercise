import logo from './logo.svg';
import './App.css';
import food1 from './food1.jpg'
import Card from './Card.js'
import { Eventhandling, Eventhandle } from './Event-handeling.js';



function Header(){
  return <h1>HELLOOO WORLD</h1>
}
function App() {
  return <Header/>
} 

function Heading (){
  let title = 'This is how we do it'
  return <h1>{title}</h1>;//if we had type <h1>title</h1> it would have displayed 'title'
}

//this part is to insert the food1.jpg image
function Pic(){
  const image ={
    height: "120px",
    width: "120px",
    display: "flex", 
  }
  const result = <img src={food1} style={image}/>
  return result
}

function Happ() {//this is class assignment
  return (
    <div className='Appp'>
      <h1>Task: Add three Card elements</h1>
      <Card  h2="First card's h2"  h3="First card's h3"/>
      <Card h2="Second card's h2" h3="Second card's h3" />
      <Card h2= "Third card's h2" h3= "Third card's h3"/>
    </div>
  );
}

function Appp(){
  const imgdiv = {//This part is to style the image container className='imge'
    display: "flex",
    width: "100%",
    height: "fit-content",
    justifyContent: "center",
  }
  return (<div className="container">
            <div>
              <App/>
            </div>
            <div>
              <Heading/>
            </div>
            <div className='imge' style={imgdiv} >
              <Pic />
            </div>
            <div>
              <Happ/>
            </div>
            <div>
              <Eventhandling/>
            </div>
            <div>
              <Eventhandle/>
            </div>
          </div>) 
}

export default Appp