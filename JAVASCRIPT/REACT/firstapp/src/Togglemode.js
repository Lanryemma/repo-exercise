function Togglemode(){
    let DarkModeOn = true;
    const DarkMode = <h2>This is darkmode</h2>;
    const LightMode = <h2>This is Lightmode</h2>
    const Toggle = ()=>{
         DarkModeOn = !DarkModeOn;
         let condition = DarkModeOn === true ? "The Dark Mode is on" : DarkModeOn === false ? "The Light Mode is on":"Tis is not a boolean"
         console.log(condition)
    }
    
 return (//now we add a if statement to check if darkMode is on
    <div>
        <button onClick={Toggle}>
            Dark click
        </button>
        <div className="Mode">
            {DarkModeOn ? DarkMode : LightMode}
        </div>
    </div>
   
 )//we need to change the value of DarkModeOn to see the real effect in'Mode'
}

export default Togglemode