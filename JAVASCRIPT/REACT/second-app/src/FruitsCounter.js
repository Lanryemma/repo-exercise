function FruitsCounter(props) {
    const fruit = props.state;
       return (
           <h2>Total fruits: {fruit.length} </h2>
       )
   }
   
   export default FruitsCounter;