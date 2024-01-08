import { useState } from "react"

//UNCONTROLLED FORM
const Form = ()=> {
    return(
        <div>
            <h4>UNCONTROLLED FORM</h4>
            <form>
                <fieldset>
                    <div className="Field">
                        <label>
                            EntetName:
                            <input type="text"  placeholder="Full Name" name="name"/>
                        </label>
                    </div>
                    <button type="submit">submit</button>
                </fieldset>
            </form>
        </div>
    )
}

export {Form}


//CONTROLLED FORM
const Form1 = ()=> {
    const [contol, setcontrol] = useState('')
    const handleSubmit = (e)=>{
        //to prevent my form trying to submit it to the server
        e.preventDefault()
        //to indicate the form has been submitted
        console.log("Submitted Successfully")
        //to reset the form after pressing the submit button
        setcontrol("")

    }
    return(
        <div>
            <h4>CONTROLLED FORM</h4>
            <form onSubmit={handleSubmit}>
                <fieldset>
                    <div className="Field">
                        <label htmlFor="names">EntetName:</label>
                        <input type="text"  placeholder="Full Name" id="names"value={contol} onChange={(e)=> setcontrol(e.target.value)}/>
                    </div>
                    <button type="submit" disabled={!contol}>submit</button>
                </fieldset>
            </form>
        </div>
    )
}

export {Form1}



//this is a Review form
const Form2 = ()=> {
    const [score, setscore]= useState("")
    const[comment, setcomment]= useState("")
    function handsubmit(e){
        e.preventDefault();
        if(Number(score)<=5 && comment.length<=10){
            alert("please provide an explaination why your rating was poor ")
            return;
        }
        console.log('submitted successfully')
        setscore(0)
        setcomment("")
    }
    return(
        <div>
            <h4>A REVIEW FORM</h4>
            <form onSubmit={handsubmit}>
                <fieldset>
                    <h4>FEEDBACK FORM</h4>
                    <div className="Field2">
                        <label htmlFor="namess">
                            Score: {score}
                        </label>
                        <input type="range" min='0' max='10' name="namess" id="namess" 
                        value={score} onChange={(e)=> setscore(e.target.value)}/>
                    </div>
                    <div className="Field3">
                        <label>Comment </label>
                        <textarea value={comment} onChange={(e)=> setcomment(e.target.value)}/>
                    </div>
                    <button type="submit">submit</button>
                </fieldset>
            </form>
        </div>
    )
}

export {Form2}