//Now we ar going to add the product object from the the app component in App.js
//using the Props element of React
function Promo(props) {
    return (
        <div className="promo-section">
            <div>
                <h1>NEW!! {props.product},Don't miss this deal!</h1>
            </div>
            <div>
                <h2>Subscribe to my newsletter and get all the shop items at 50% off!</h2>
            </div>
        </div>
    );
};

export default Promo;