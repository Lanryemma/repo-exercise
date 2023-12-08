import logo from './logo.svg';
import './App.css';
import Intro1 from './Intro1';
import Intro2 from './Intro2';
import Intro3 from './Intro3';
import Nav from './Nav';
import Promo from './Promo';
import Footer from './Footer';

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
    </div>
  );
}

export default App;
