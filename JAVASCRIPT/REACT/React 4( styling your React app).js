//There are various ways to style JSX elements.
//the simplest way to do this is using the link HTML element in the head of the 
//index.html file in which your React app will mount.

//The href attribute loads some CSS styles
//inside the function component's declarations, you can access those CSS classes 
//using the className attribute.
function Promo(props) {
    return (
        <div className="promo-section">
            <div>
                <h1>{props.heading}</h1>
            </div>
            <div>
                <h2>{props.promoSubHeading}</h2>
            </div>
        </div>
    );
}
//In CSS:
/*.promo-section {
    font-weight: bold;
    line-height: 20px;
}*/


//Another way to add CSS styles to components is using inline styles.
//Consider a starting Promo component
function Promoo(props) {
    return (
        <div className="promo-section">
            <div>
                <h1 style={{color:"tomato", fontSize:"40px", fontWeight:"bold"}}>
                    {props.heading}
                </h1>
            </div>
            <div>
                <h2>{props.promooSubHeading}</h2>
            </div>
        </div>
    );
}

export default Promoo;

//You can then re-write this object literal:
//Additionally, since it's just JavaScript, those CSS properties that would be hyphenated 
//in plain CSS, such as, for example, font-size:40px, become camelCased, and the value is a 
//string, making it look like this: fontSize:"40px"
/*{
    color: "tomato",
    fontSize: "40px"
}*/
function Prom(props) {

    const styles = {
        color: "tomato",
        fontSize: "40px"
    }
    
    return (
            <div className="promo-section">
                <div>
                    <h1 style={styles}>
                        {props.heading}
                    </h1>
                </div>
                <div>
                    <h2>{props.promoSubHeading}</h2>
                </div>
            </div>
        );
    }