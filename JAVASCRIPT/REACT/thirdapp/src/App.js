import logo from './logo.svg';
import './App.css';
import { AboutMe } from './AboutMe';
import { Homepage } from './Homepage';
import { Routes, Route, Link } from 'react-router-dom';
import Contact from './Contact';

function App() {
  return (
    <div className="App">
      <nav className='nav-bar'>
        <Link to='/ Home.me' className='nav-item'>Homepage</Link>
        <Link to='/ About.me' className='nav-item'>Aboutme</Link>
        <Link to='/ contact' className='nav-item'>Contact Us</Link>
      </nav>
      <Routes>
        <Route path="/ Home.me" element={<Homepage/>}/>
        <Route path="/ About.me" element={<AboutMe/>}/>
        <Route path="/ contact" element={<Contact/>}/>
      </Routes>
    </div>
  );
}

export default App;
