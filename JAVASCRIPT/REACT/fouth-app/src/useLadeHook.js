import { useEffect } from "react";

//This is my first Hook to consolelog the current State of App
export default function useLadeHook( currentValue){
    //We know we have to use the useEffect hook to use something like console in React without
    //having any side effect
    useEffect(() =>{
        return console.log(currentValue)
    }, [currentValue])
}