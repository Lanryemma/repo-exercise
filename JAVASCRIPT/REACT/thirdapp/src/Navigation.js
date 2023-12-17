//Before the advent of modern JavaScript frameworks, 
//most websites were implemented as multi-page applications. 
//That is, when a user clicks on a link, the browser navigates to a new webpage
//If your website is complex, it may appear slow to your users, 
//even slower if they have a slow or limited internet connection

import { BrowserRouter } from "react-router-dom";

//To solve this problem, 
//many web developers develop their web applications as Single Page Applications.
//A Single Page Application allows the user to interact with the website without 
//downloading entire new webpages. 
// it rewrites the current webpage as the user interacts with it

/*There are two approaches to serving code and resources in Single Page Applications.
@ BUNDLING :- When request it returns and load all necessary HTML, CSS and JavaScript immediately
@ LAZY LOADING or code splitting.:- When request it returns only the minimum HTML, 
  CSS and JavaScript needed to load the application*/


//To use the navagation link in React we need to Download the React Router
//1. type -[npm i react-router-dom@6]
//2. go to index.js and import the {BrowserRouter} from 'react-router-dom'
//3. in the same index.js wrap the App in BrowserRouter 
/*<BrowserRouter/>
      <App/>
  <BrowserRouter/>*/

//4. now we have to (import {Routes, Route, Link} from 'react-router-dom') to the App.js
