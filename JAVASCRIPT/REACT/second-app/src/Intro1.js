//Now we ar going to add the 'News' object from the the app component in App.js
//using the Props element of React
//we use 'pros' just to show that we can use anythingd to represent 'props'
function Intro1(Pros){
    return(
        <div class="blog-post-intro">
            <h2>{Pros.News}!!, I've become a React Developer!!</h2>
            <div>
                <p>I've Completed the React BAsic course and i am happy to announce that i am now a Junior React Developer</p>
                <p class="Link">Read more......</p>
            </div>
        </div>
    )
}

export default Intro1;