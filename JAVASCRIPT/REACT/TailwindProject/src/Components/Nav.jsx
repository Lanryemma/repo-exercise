import React from 'react'
import { useState } from 'react'
import {headerLogo} from '../assets/images'
import { navLinks } from '../Constants/Index'
import { hamburger } from '../assets/icons'


export const Nav = () => {
  const[checking,setchecking]=useState(false)
  const ClickHamburger =()=>{
    setchecking((prev)=>(!prev))
  }
  const rotatebuger = checking ? {transform: 'rotate(90deg)'
  }: {}
  return (
    <header className='padding-x py-8 z-10 absolute w-full'> 
      <nav className='flex justify-between items-center max-container max-sm:flex-wrap'>
        <a href='/' className=' relative flex items-start ml-[24px] mr-[24px] max-sm:mr-[8px]'>
          <img  src={headerLogo}
          alt='Nike Logo'
          width={130}
          height={30}
          />
        </a> 
        <ul className='flex-1 flex justify-center items-center gap-16 max-md:hidden'>
         {navLinks.map((item)=>(
          <li key={item.label} className=' text-center '>
            <a href={item.href} className='font-montserrat leading-normal
             text-md text-slate-gray border-b-2'>
              {item.label}
            </a>
          </li>
         ))}
      </ul>
      <div className='flex gap-2 text-md leading-normal font-medium 
      font-montserrat max-md:hidden ml-8 mr-[-10px]
       bg-red-500 p-4 rounded-[20px]'>
          <a href='/' className='text-white'>Sign in</a>
          <span></span>
          <a href='/'className='text-white'>Explore now</a>
        </div>
        <div className='hidden gap-2 text-sm leading-normal 
        font-medium font-montserrat max-md:block ml-4 mr-[2px]
         bg-red-500 p-2 px-3 rounded-[20px] max-sm:mt-4'>
          <a href='/' className='text-white'>Sign in</a>
        </div>
        <div className='hidden gap-2 text-sm leading-normal 
        font-medium font-montserrat max-md:block ml-2 mr-[4px]
         bg-red-500 p-2 px-3 rounded-[20px] max-sm:my-4'>
          <a href='/'className='text-white'>Explore now</a>
        </div>
        <div className='max-md:ml-8 max-sm:ml-2'>
          <img src={hamburger} style={rotatebuger} onClick={ClickHamburger} alt='menu' 
             className='h-[25px] w-[25px] hidden max-md:block'/>
            {checking && (
            <div className='h-fit w-fit  px-2 border-2 border-[slate-gray] right-0 
            absolute bg-white rounded-[10px] hidden max-md:block'> 
              <ol>
                {navLinks.map((item) => (
                  <li key={item.label} className='pb-2'>
                    <a
                      href={item.href}
                      className='font-montserrat leading-normal text-lg text-coral-red border-b-2 '
                    >
                      {item.label}
                    </a>
                    <br />
                  </li>
                ))}
              </ol>
            </div>  
              )}
        </div>
      </nav>
    </header>
    
  )
}
