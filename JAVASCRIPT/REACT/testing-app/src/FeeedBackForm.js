import {useState} from 'react'

export default function FeeedBackForm({onSubmit}){
  const [score, setscore]= useState('10')
  const [comment, setcomment]= useState('')

 const isDisabled = Number(score) < 5 && comment.length <= 10;
 const TestFeedback = isDisabled ? `please write a more detailed feedback 
 comment about why you rated the restaurant soo low`: `you can provide a feedback comment if you want`

const Handlesubmit=(e)=>{
    e.preventDefault();
    onSubmit({score,comment})/*'score' and 'comment' is passed as props incase you want to give
    you want to submit the formbased on a condition*/
}
 //This is the final output of the feedback form
 return (
    <div className='feedbackapp'>
        <form onSubmit={Handlesubmit} >
            <fieldset>
                <h2>FeedBack Form</h2>
                <div className='Rating'>
                    <label htmlFor='rating'style={{display: "block"}}>Score: {score}</label>
                    <input type='range' value={score} name='rating' id='rating'
                    onChange={(e)=> setscore(e.target.value)}
                    min='0'
                    max='10'/>
                </div>
                <div className='Commenting'>
                    <label htmlFor='comment'style={{display: "block"}}>comments:</label>
                    <textarea placeholder={TestFeedback} 
                    value={comment} name='comment' id='comment'
                    onChange={(e)=> setcomment(e.target.value)}
                    />
                </div>
                <button type='submit' disabled={isDisabled} style={{color: "white",backgroundColor: "blue", borderRadius: "4px"}}>
                    submit
                </button>
            </fieldset>
        </form>
    </div>
 )
}