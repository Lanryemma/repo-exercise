//In this code we are going to Manipulate component children dynamically
import {cloneElement,Children} from 'react'
//Using this powerful React APIs - 'React.cloneElements' and 'React.children'

//imagine little lemon wants to craet an order board that stores live orders
function OrderBoard({children, spacing}){
    const ChildStyle = {
        marginLeft: `${spacing}px`
    }
    return (
        <div>
            {Children.map(children, (child,index)=>{
                return cloneElement(child, {
                    style: {
                        ...child.props.style ,
                        ...(index > 0 ? ChildStyle : {} )
                    },
                })
            })}
        </div>
    )
}

//The life order contain the "food","Howmany","price","The time of Order" and the "Customers name"
export function LiveOrder (){
    return(
        <div>
            <OrderBoard spacing = {32}>
                <p>Falafel</p>
                <p>3</p>
                <p>30$</p>
                <p>10:31am</p>
                <p>James</p>
            </OrderBoard>
        </div>
        
    )
}

