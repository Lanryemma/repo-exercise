import logo from './logo.svg';
import './App.css';
import { AboutMe } from './AboutMe';
import { Homepage } from './Homepage';
import { Routes, Route, Link } from 'react-router-dom';
import Contact from './Contact';
import { LogicalAndExample } from './Conditional-rendering';
import { Myapp } from './Conditional-rendering';
import {Image1, Image2} from './images'
import React from "react";
import ReactPlayer from "react-player/youtube";
import { Audo } from './Media package';
import { VideoPlayer } from './Media package';

function Vidd(){
  const VidUrl = "https://www.youtube.com/watch?v=ysz5S6PUM-U"
  return (
    <div>
      <h3>This a the Video Example for React</h3>
      <ReactPlayer url ={VidUrl} playing={false} volume={0.5} height={150} width={150}/>
    </div>
  )
}


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
      <div>
        <LogicalAndExample/>
      </div>
      <div>
        <Myapp/>
      </div>
      <div>
        <Image1/>
      </div>
      <div>
        <Image2/>
      </div>
      <div>
        <Vidd/>
      </div>
      <div>
        <Audo/>
      </div>
      <div>
        <VideoPlayer/>
      </div>
    </div>
  );
}

export default App;
