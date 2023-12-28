//applying conditional Rendering
/*function CurrentMessage() {
         const day = new Date().getDay();
        if (day >= 1 && day <= 5) {
             return <Workdays />
        }
         return <Weekends />
    }


//if the component was a child
function CurrentMessage(props) {
        if (props.day >= 1 && props.day <= 5) {
            return <Workdays />
        }
        return <Weekends />
    }


//Conditional rendering with the help of element variables
//Here’s an example of doing this with the CurrentMessage component:
function CurrentMessage({day}) {
     const weekday = (day >= 1 && day <= 5);
     const weekend = (day >= 6 && day <= 7);
    let message;
    
    if (weekday) {
         message = <Workdays />
        } else if (weekend) {
        message = <Weekends />
        } else {
          message = <ErrorComponent />
        }
    
        return (
           <div>
                {message}
           </div>
        )
    }    
*/

//Conditional rendering using the logical AND operator
export function LogicalAndExample() {
        const val = prompt('Anything but a 0')
    
        return (
            <div>
                <h1>Please don't type in a zero</h1>
                {val &&
                <h2>Yay, no 0 was typed in!</h2>
              } 
            </div>
        )
}

/*
//To understand what will be output on screen, 
//consider the following example in standard JavaScript

 [true && console.log('This will show')]
//If you ran this command in the browser’s console, the text ‘This will show’ will be output.

//On the flip side, consider the following example:
[false && console.log('This will never show')]
//If you ran this command, the output will just be the boolean value of false.*/



//Conditional components
//For example, you can set a variable to a different value based on the result of a condition check.
let name; 
let newUser = true; 
if (Math.random() > 0.5 && newUser) { 
	name = "Mike" 
} else { 
	name = "Susan" 
} 

//Let’s take a look at a simple example of simple login and out button
/*function LogInOutButton(props) {
    const isLoggedIn = props.isLoggedIn;
      if (isLoggedIn) {
        return <LogoutButton />;
      } else {
      return <LoginButton />;
    }
}
//Then when the LogInOutButton parent component is used, the prop can be passed in.
<LogInOutButton isLoggedIn={false} />*/



//THIS IS AN APP THAT DISPLAYS DIFFERENT MESSAGES BASED ON THE DAY
export function Myapp(){
    const time = new Date();
    const  day = time.toLocaleString("en-us", {weekday:"long"});
    const morning = time.getHours()>=6 && time.getHours() <=12;
    let Daymessage

    if (day.toLocaleLowerCase() === 'monday'){
        Daymessage = `Happy ${day}`
    }else if(day.toLocaleLowerCase() === 'tuesday'){
        Daymessage = `${day}, four days to go`
    }else if(day.toLocaleLowerCase() === 'wednesday'){
        Daymessage = `${day}, half way there`
    }else if(day.toLocaleLowerCase() === 'thursday'){
        Daymessage = `${day}, start planning the weekend`
    }else if(day.toLocaleLowerCase() === 'friday'){
        Daymessage = `woo - hoo, The weekend is already here`
    }else{
        Daymessage = `Have fun and relax`
    }
     return (
        <div>
            <h3>{Daymessage}</h3>
            {morning? <h3>Have your Breakfast to have enough energy</h3>:''}
        </div>
     )
}