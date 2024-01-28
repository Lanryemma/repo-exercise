import logo from './logo.svg';
import './App.css';
import FeeedBackForm from './FeeedBackForm';

const FinalSubmit=()=>{
  console.log("Feedback submitted successfully")
}

function App() {
  return (
    <div className="App">
      <FeeedBackForm onSubmit ={FinalSubmit}/>
    </div>
  );
}

export default App;
