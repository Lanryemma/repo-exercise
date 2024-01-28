import  {useState,useEffect} from 'react';

const DataFetcher =( {render,Url})=>{
    const [Data,setData]= useState([])
    useEffect(()=>{
        if(Url.includes('desserts')){
            setData(['cake','ice-cream', 'pie', 'Brownies','waffles'])
        }else{
            setData(['water','Champagne','smoothy','Soda','Coffee'])
        }
    }, [Url])
    
    return render(Data)
}

const DessertCount =()=>{
    return <DataFetcher render={(Data)=> (<p>{Data.length} desserts available</p>)}
     Url='https://LittleLemon/desserts'/>

}

const DrinkCount =()=>{
    return <DataFetcher render={(Data)=> (<p>{Data.length} drinks available</p>)}
     Url='https://LittleLemon/drinks'/>

}

export const RenderDisplay =()=>{
    return (
        <div>
             <DessertCount/>
            <DrinkCount/>
        </div>
    )
}
//=========================================================================================================


const MousePosition = ({ render }) => {
    const [mousePosition, setMousePosition] = useState({
      x: 0,
      y: 0,
    });
  
    useEffect(() => {
      const handleMousePositionChange = (e) => {
        // Use e.clientX and e.clientY to access the mouse position on the screen
        setMousePosition({
          x: e.clientX,
          y: e.clientY,
        })
      };
  
      window.addEventListener("mousemove", handleMousePositionChange);
  
      return () => {
        window.removeEventListener("mousemove", handleMousePositionChange);
      };
    }, []);
  
    // What should be returned here?
    return render(mousePosition);
  };
  
  // This component should not receive any props
  const PanelMouseLogger = () => {
    // The below if statement can be removed after the render props pattern is implemented
    
    return (<MousePosition render={(mousePosition) => (
      <div className="BasicTracker">
        <p>Mouse position:</p>
        <div className="Row">
          <span>x: {mousePosition.x}</span>
          <span>y: {mousePosition.y}</span>
        </div>
      </div>)
      } />
     
    );
  };
  
  // This component should not receive any props
  const PointMouseLogger = () => {
    // The below if statement can be removed after the render props pattern is implemented
    return (<MousePosition render={(mousePosition) => (
      <p>
        ({mousePosition.x}, {mousePosition.y})
      </p>)
    }/>
    )
  };
  
  export function RenderMouseApp() {
    return (
      <div className="RenderApp">
        <header className="Header">Little Lemon Restaurant 🍕</header>
        <PanelMouseLogger />
        <PointMouseLogger />
      </div>
    );
  }
  