//This part is to show how to use event handling in React
function Eventhandling(){
    const eventlistener = ()=>{
        console.log('You clicked me')
    }
    return (
        <div>
            <button onClick={eventlistener}>
                click me
            </button>
        </div>
    )
}

function Eventhandle(){
    const Hover = ()=>{
        console.log('you hovered over me')
    }
    return (
        <div>
            <button onMouseOver ={Hover}>
                hover and see
            </button>
        </div>
    )
}

export {Eventhandling, Eventhandle}