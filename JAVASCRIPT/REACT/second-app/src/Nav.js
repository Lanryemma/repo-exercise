//Now we ar going to add the name and color object from the the app component in App.js
//using the Props element of React
function Nav(props) {
    return (
        <nav className="main-nav">
            <ul>
                <li><a href="Home.html">Home</a></li>
                <li><a href="Article.html">Article</a></li>
                <li><a href="About.html">About</a></li>
                <li><a href="Contact.html">Contact</a></li>
            </ul>,
          <h3>{props.name},{props.Color}</h3>
        </nav>
    );
};

export default Nav;