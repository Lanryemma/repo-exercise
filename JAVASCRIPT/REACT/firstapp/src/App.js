import logo from './logo.svg';
import './App.css';

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
function app(){
  return <Heading/>
}

export default app