import React from 'react'

const Shoelist = ({imgURL, ChangebigshoeImage,bigShoeimg}) => {
    const HandleClick=()=>{
        if(bigShoeimg!=imgURL.bigShoe){
            ChangebigshoeImage(imgURL.bigShoe)
        }
       
    }
  return (
    <div className={`rounded-xl border-2
    ${bigShoeimg ===imgURL.bigShoe? 'border-coral-red':'border-transperent'}
    cursor-pointer max-sm:flex-1 `}onClick={HandleClick}>
        <div className='flex justify-center items-center 
        bg-cover bg-card bg-center md:w-[120px] md:h-[120px] sm:w-40 sm:h-40 max-sm:p-4 rounded-xl'>
            <img src={imgURL.thumbnail}
            alt='shoe-collection'
            width={127}
            height={103}
            className='object-contain'/>
        </div>
        
    </div>
  )
}

export default Shoelist