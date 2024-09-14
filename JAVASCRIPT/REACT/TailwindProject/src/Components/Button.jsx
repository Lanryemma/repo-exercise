import React from 'react'

const Button = ({label,iconURL}) => {
  return (
    <button className='flex justify-center items-center bg-coral-red px-7 py-3 
    rounded-full text-white border-coral-red font-montserrat leading-none'>
        {label}
        {iconURL && <img src={iconURL} alt='arrow icon'
        className='ml-2 rounded-full w-5 h-5'/>}
    </button>
  )
}

export default Button