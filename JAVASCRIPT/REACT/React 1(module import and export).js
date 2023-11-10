//State is simply all the values of all the variables 
//your app is working with at any given point in time.

//Module 1: Anatomy of React
/*By the end of this module you will be able to:

Explain the concepts behind React and component architecture.

Describe how to use assets within an app to apply styling and functional components.

Create a component to service a specific purpose.

Create a folder and demonstrate how to create and import files within that folder.

Use and manipulate props and components to effect visual results.*/

//Module 2: Data and State
/*By the end of this module you will be able to:

Use common methods to manage state in React.

Detail the concept and nature of state and state change.

Describe the hierarchical flow of data in React.

Describe how data flows in both stateful and stateless components.

Use an event to dynamically change content on a web page.

Describe some common errors associated with events and the syntax required to handle them.*/

//Module 3: Navigation Updating and Assets in React
/*By the end of this module you will be able to:

Use media assets, such as audio and video, with React.

Demonstrate how to manipulate image assets using reference paths.

Explain the folder structure of a React project in terms of embedded or referenced assets.

Demonstrate the conditional implementation and rendering of multiple components.

Create and implement a route in the form of a navbar.

Describe navigation design in React, with a focus on single and multi-page navigation.*/


//Module 4: Portfolio Mini-Project (Calculator App)
/*By the end of this module you will be able to:

Synthesize the skills from this course to create and style a React component.

Reflect on this course's content and on the learning path that lies ahead.*/

//JavaScript Modules
//In JavaScript, a module is simply a file
//A module can be as simple as a single function in a separate file.
//All that you would need to do to make it a JavaScript module is use the export syntax.
//Default Exports
export default function addTwo(a, b) {
    console.log(a + b);
}
//Here's an alternative syntax:
/*function addTwoo(a, b) {
    console.log(a + b);
}

export default addTwoo;*/

//Named Exports
export function addTwo(a, b) {
    console.log(a + b);
}

export function addThree(a , b , c) {
    console.log(a + b + c);
}
//Here's another way you could do it
/*function addTwo(a, b) {
    console.log(a + b);
}

function addThree(a , b , c) {
    console.log(a + b + c);
}

export { addTwo, addThree };*/


//Importing Modules
//The first module is addTwo.js and the second module is mathOperations.js.
//You want to import the addTwo.js module into the mathOperations.js module.
// exporting the addTwo function as a default module
// addTwo.js module:
/*function addTwo(a, b) {
    console.log(a + b);
}

export default addTwo;*/

//To import it into the mathOperations.js module
import addTwo from "./addTwo";

// the rest of the mathOperations.js code goes here

//if the addTwo function was instead a named export:
import { addTwo } from "./addTwo";

// the rest of the mathOperations.js code goes here
