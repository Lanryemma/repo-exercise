//This file will contain instructions on how to install 
//the reactjs-media npm package for video and Audio

//To install this package you'll need to use the following command in the terminal:
//(npm install react-player)

//Once you have this package installed, you can start using it in your project.
//(import ReactPlayer from "react-player";)

//for example, only planning to use videos from a site like YouTube, 
//to reduce bundle size, you can use the following import:
//(import ReactPlayer from "react-player/youtube";)

//Here’s an example of using the react-player packaged in a small React app:
import React from "react";
import ReactPlayer from "react-player/youtube";


const Vid = () => {
  return (
    <div>
      <MyVideo />
    </div>
  );
};

const MyVideo = () => {
  return (
    <ReactPlayer url='https://www.youtube.com/watch?v=ysz5S6PUM-U' />
  );
};

export  {Vid};

//this part to a class project on a audio pause and play
//import React from "react";

function Audo() {

  const bird1 = new Audio(
    "https://upload.wikimedia.org/wikipedia/commons/9/9b/Hydroprogne_caspia_-_Caspian_Tern_XC432679.mp3"
  );

  const bird2 = new Audio(
    "https://upload.wikimedia.org/wikipedia/commons/b/b5/Hydroprogne_caspia_-_Caspian_Tern_XC432881.mp3"
  );

  function toggle1() {
    if (bird1.paused) {
      bird1.play();
    } else {
      bird1.pause();
    }
  };

  function toggle2() {
    if (bird2.paused) {
      bird2.play();
    } else {
      bird2.pause();
    }
  };


  return (
    <div>
      <button onClick={toggle1}>Caspian Tern 1</button>
      <button onClick={toggle2}>Caspian Tern 2</button>
    </div>
  );
}

export {Audo};

const VideoPlayer = () => {
  const videoUrl = './Asset/Videoo.mp4';

  return (
    <div>
      <ReactPlayer
        url={videoUrl}
        controls={true} // Show video controls
        width="100%"    // Set the width of the player
        height="auto"   // Automatically adjust the height based on the aspect ratio
      />
    </div>
  );
};
export {VideoPlayer}

/*<ReactPlayer
  playing
  url={[
    {src: 'foo.webm', type: 'video/webm'},
    {src: 'foo.ogg', type: 'video/ogg'}
  ]}
/>*/