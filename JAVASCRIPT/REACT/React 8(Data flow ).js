//Parent - child Relationship
function Promoheading(props){//Ths is a child component
    return (
        <div>
            <h2>{props.heading1}</h2>
            <h2>{props.heading2}</h2>
        </div>
    )
}
//export default Promoheading

//import Promoheading from "./Promoheading"
function Promo(){//This is the parent component
    const data = {
        promo: "80% off on all Our items",
        speach: "We will be opened for sales from the 26th of December"
    }
    return(
        <div>
            <Promoheading heading1={data.promo} heading2={data.speach} />
        </div>
    )
}
/*======================================================================================================*/

//Here’s a practical example of this:

//Parent component:
function Dog() {
    return (
        <Puppy name="Max" bowlShape="square" bowlStatus="full" />
    );
};

//Child component
function Puppy(props) {
    return (
        <div>
            {props.name} has <Bowl bowlShape="square" bowlStatus="full" />
        </div>
    );
};

//Grandchild component:
function Bowl(props) {
    return (
        <span>
            {props.bowlShape}-shaped bowl, and it's currently {props.bowlStatus}
        </span>
    );
};
/*============================================================================================*/

//CHILDREN AND DATA
//Props helps the parent component render data in the child component
//props is data outside the component so it cannot be changed by the component
//state is data inside the componnt and can be changed by the componnet

//EXAMPLE
function Currenttime(props){//this is the child component
    return(
        <div>
            <h2>{props.realtime}</h2>
        </div>
    )
}
//export default Currenttime

function New(){//this is the parent component
    const date = new Date()
    return(
        <div>
            <Currenttime realtime = {date}/>
        </div>
    )
}
/*=================================================================================================*/

