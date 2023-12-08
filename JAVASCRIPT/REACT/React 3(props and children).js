//in this example we consider a bag as an independent conponent
//it an carry pears or apples but neither a pear or an apple bag 
function Apples(props) {
     return (
        <div className="promo-section">
            <div>
                <h2>These apples are: {props.color}</h2>
                </div>
                <div>
                <h3>There are {props.number} apples.</h3>
            </div>
        </div>
     )
    }
    //export default Apples

    function Pears(props) {
         return (
            <h2>I don't like pears, but my friend, {props.friend}, does</h2>
         )
        }

 //You can define a Bag component as follows:
 function Bag(props) {
    const bag = {
        padding: "20px",
        border: "1px solid gray",
        background: "#fff",
        margin: "20px 0"
    }
    return (
        <div style={bag}>
            {props.children}
        </div>
    )
}
//export default Bag
//So, what this does in the Bag component is: it adds a wrapping div with a specific styling, 
//and then gives it props.children as its content.

function show(){//this is just to show the different examples without showing error
    return (
        <div>
            //Here's how you'd render the Bag component with the Apples component as its props.children:
            <Bag children={<Apples color="yellow" number="5" />} />

            //And here's how you'd render the Bag component, wrapping the Pears component:
            <Bag children={<Pears friend="Peter" />} />


            /*Effectively, the above syntax is the same as the two examples below.*/
            <Bag>
                <Apples color="yellow" number="5" />
            </Bag>

            <Bag>
                <Pears friend="Peter" />
            </Bag>

            //You can even have multiple levels of nested JSX elements, 
            or a single JSX element having multiple children
            <Trunk>
                <Bag>
                    <Apples color="yellow" number="5" />
                    <Pears friend="Peter" />
                </Bag>
            </Trunk>
            //So, in the above structure, there's a Trunk JSX element, 
            inside of which is a single Bag JSX element, holding an Apples and a Pairs JSX element.
        </div>
    )
}
