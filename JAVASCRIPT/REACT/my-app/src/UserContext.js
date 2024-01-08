//We will use Context API to pass data from 
//components to componenets without using props
import { createContext, useContext, useState } from "react";

export const UseContext = createContext(undefined);

export const Userprovider = ({children})=>{
    const[user] = useState({
        name:"Olayokun OLolade",
        email: "Lanryemma@gmail.com",
        Dob: "12/07/2000"
    })
    return (<UseContext.Provider value={{user}}>
                {children}
            </UseContext.Provider>)
}

export const useUser = ()=> useContext(UseContext)

//This part is for the example html

