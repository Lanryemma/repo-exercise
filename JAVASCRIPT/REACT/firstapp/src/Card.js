//this is card component
function Card(prop) {
    return (
        <div className ="card">
            <h2>{prop.h2}</h2>
            <h3>{prop.h3}</h3>
        </div>
    )
}

export default Card