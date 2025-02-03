import React, { useState } from 'react'
import Button from '../Components/Button'
import { arrowRight } from '../assets/icons'
import { shoes, statistics } from '../Constants/Index'
import { bigShoe1 } from '../assets/images'
import Shoelist from '../Components/Shoelist'

const Hero = ()=> {
  const rotatebuger = {transform: 'rotate(15deg)'}
  const[bigShoeimg, setbigShoeimg]= useState(bigShoe1)

  return (
    <section id='home' className='w-full xl:flex-row flex-col 
        justify-center min-h-screen gap-10
        border-y-2 border-red-500 p-5 pl-8'>
      <div className='relative xl:w-2/5 flex
       flex-col justify-center items-start w-full 
       max-xl:padding-x pt-28 max-sm:mt-[30px]'>
        <p className='text-xl font-montserrat max-sm:mt-[20px] text-coral-red'>Our Summer Collection</p>
        <h1 className='mt-10 font-palanquin text-8xl font-bold max-sm:text-[65px] max-sm:leading-[75px]'>
          <span className='xl:bg-white xl:whitespace-nowrap 
          relative z-10 pr-10'>The New Arrival</span><br/>
          <span className='text-coral-red inline-block mt-3 '>Nike</span><span> Shoes</span>
        </h1>
        <p className='text-lg font-montserrat my-4 text-slate-gray leading-8 sm:max-w-sm max-sm:text-sm '>Discover stylish Nike arrivals, quality comfort,
          and innovation for your active life
        </p>
        <Button label='Shop now' iconURL={arrowRight}/>
        <div className='flex justify-start items-start w-full flex-wrap mt-20 gap-16'>
          {statistics.map((stats) =>(
            <div key={stats.label}>
              <p className='text-4xl font-palanquin font-bold max-sm:text-[38px] max-sm:leading-[28px]'>{stats.value}</p>
              <p className='leading-7 text-slate-gray font-montserrat'>{stats.label}</p>
            </div>
          ))}
        </div>
      </div>
      
      <div className='relative flex flex-1 justify-center items-center 
      bg-cover bg-primary bg-center bg-hero xl:min-h-screen max-lg:py-40 max-h-screen'>
        <img src={bigShoeimg} 
        style={rotatebuger}
        alt='shoe collection'
        width={500}
        height={400}
        className='relative z-10 object-contain lg:top-[-2%]'/>
        <div className=' sm:gap-6 gap-4 absolute flex xl:-bottom-[2%] -bottom-[15%] 
        max-sm:-bottom-[5%] z-10 max-sm:px-6 sm:left-[10%]'>
          {shoes.map((shoe)=>(
            <div key={shoe}>
              <Shoelist imgURL={shoe} ChangebigshoeImage={(shoe)=>{ setbigShoeimg(shoe)}} bigShoeimg={bigShoeimg}/>
            </div>
            
          ))}
        </div>
      </div>
    </section>
  )
}

export default Hero