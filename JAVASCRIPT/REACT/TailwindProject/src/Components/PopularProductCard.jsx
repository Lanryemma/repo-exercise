import React from 'react'
import { star } from '../assets/icons'

const PopularProductCard = ({imgURL, name, price}) => {
  return (
    <div className='flex flex-1 flex-col w-full max-sm:w-full'>
        <img src={imgURL}
        alt={name}
        className='w-[280px] h-[280px]'/>
        <div className='mt-4 flex justify-start gap-2.5' width={24} height={24}>
            <img src={star} alt="ratings"/>
            <p className='font-monstserrat text-slate-gray text-xl leading-normal'>(4.5)</p>
        </div>
        <h3 className='leading-normal text-xl font-semibold font-palanquin mt-4'>{name}</h3>
        <p className='mt-2 font-montserrat text-coral-red leading-normal'>{price}</p>
    </div>
  )
}

export default PopularProductCard