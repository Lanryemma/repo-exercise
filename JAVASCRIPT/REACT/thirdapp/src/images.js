import falafel from './Assets/Falafel.jpeg'

const Image1 = ()=>{
    return (
        <div>
            <h3>This is the first method</h3>
            <img height={150} src= {falafel} alt='image of falafel' />
        </div>
    )
}

const Image2 = ()=>{
    return (
        <div>
            <h3>This is the second method</h3>
            <img src= {require('./Assets/Falafel.jpeg')} alt='image of falafel' style={{height: "150px"}}/>
        </div>
    )
}

export {Image1, Image2}

//This is the third method
const UsingUrl = 'http//coursera/images .png'
const Image3 = ()=>{
    return (
        <div>
            <h3>This is the third method</h3>
            <img src={UsingUrl}  style={{height: "150px"}}/>
        </div>
    )
}