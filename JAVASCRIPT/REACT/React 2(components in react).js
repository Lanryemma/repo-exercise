//REACT
//used to build and compose components
//High performance rendering
//component rendering
//a React component acts much like a traditional JavaScript function
//React provides two types of components, functional components and class components.

//functional components act like a javascript function
//for example
function welcome (){
    return <h1>'hello'</h1>
}
//to render components in react we use this syntax
<ComponentName></ComponentName>
//React is scripted using a special syntax called JavaScript XML or JSX
//JSX allows you to write JavaScript code inside what looks like HTML elements. 
//In fact, you can think of JSX as a combination of custom HTML and JavaScript
//It's important to remember that all component names in React must be capitalized
//because React treats lowercase components as regular HTML elements
//for example .... Heading.js.....
//component example
function Heading (){
    let title = 'This is how we do it'
    return (<h1>{title}</h1>);//if we had type <h1>title</h1> it would have displayed 'title'
}
//now to display it
function app(){
    return <Heading/>
}

//Transpiling
//transpiling is a process of converting JSX to HTML

//to create new react file we use this commands
//first on the terminal run: npm init react-app (whatever name you want to give to ur app)
//npx create-react-app my-app
//then you'll run: cd firstapp
//finally you'll run:  npm start