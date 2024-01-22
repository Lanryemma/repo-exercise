import  { useEffect,useState } from 'react'
function RainBow(WrappedComponent){
    const ColorArray = ['red', 'blue','gold','green', 'purple','orange'];
    const TColor = ()=> ColorArray[Math.round(Math.random()*5)]
    return (props)=>{
    return <WrappedComponent  TColor={TColor}{...props} />;
  };
     /*return(
        <WrappedComponent Tcolor ={Tcolor} {...props}/>
     ) 
    };*/
 }


const ConsumerComponent =(props)=>{
  const [styleColor , setstyleColor] = useState({color: ""})
  const FlickColor =()=>{
    setstyleColor({color: props.TColor()})//this is to enable it to rerender anytime the button is clicked
  }
  return (
    <>
        <h3 style={styleColor}>When i click the button below the color of this text os going to change<br/>
           isnt this amazing im just trying to use higerOrder components</h3>
        <button onClick={FlickColor}>
            FlickColor
        </button>
    </>
  )
}
const FianlRender = RainBow(ConsumerComponent)

export const HigherOrderDisplay =()=>{
    return (
        <FianlRender/>
    )
}



//This is a Higher Order component to track mouse position

//to harness the mouseposition
 const CatchMousePosition =(WrapComponent)=>{
    const [position, setposition] = useState({
        x: 0,
        y:0,
    });
     useEffect(()=>{
            const MouseChange =(e)=>{
                setposition({
                    x: e.clientX,
                    y: e.clientY,
                })
            } 
            window.addEventListener('mousemove',MouseChange)
        return()=>{
            window.removeEventListener('mousemove',MouseChange)
        }
     },[])
   return(props)=>{
    return <WrapComponent mousePosition={position} {...props}/>
   }
 }

const PanelLogger =({mousePosition})=>{
    if(!mousePosition){
        return null
    }
    return (
        <div>
            <p>Moise Position</p>
            <div>
                <span>X: {mousePosition.x}</span>
                <span>Y: {mousePosition.y}</span>
            </div>
           
        </div>
    )
}
const PositionLogger =({mousePosition})=>{
    if(!mousePosition){
        return null
    }
    return (
        <div>
            <p>({mousePosition.x} ,{mousePosition.y})</p>
        </div>
    )
}

const PositionTracker = CatchMousePosition(PositionLogger)
const PanelTracker = CatchMousePosition(PanelLogger)

export function MouseApp(){
    return (
        <div className='MouseApp'  style={{marginTop: "50px"}}>
            <header className='Header'>My mouse Tracking App &#x1F401;</header>
            <PanelTracker/>
            <PositionTracker/>
        </div>
    )
}
