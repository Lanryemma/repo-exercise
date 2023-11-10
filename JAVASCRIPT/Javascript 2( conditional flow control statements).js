//This project is for conditional statements 
var result = 50
//result = 39 // this part is to change the value of "result" to show the person failed
if (result >= 40){
    console.log("congratulations you passed the test")
} else {
    console.log("im sorry but you failed the test")
}

// when the are multiple statement to choose from,
// you use the else if statement
var place = "Third"
if (place == "first"){
    console.log("You won the Gold medal")
}else if (place == "second"){
    console.log("You won the Silver medal")
}else if (place == "Third"){
    console.log("You won the Bronze medal")
}else {
    console.log("You won No medal")
}

// when the are multiple statement to choose from,
// you also use the "switch (case/default)" statement
var position = "second"
switch(position){
    case "first":
        console.log("GOLD");
        break;
    case "second":
        console.log("SILVER");
        break;
    case "third":
        console.log("BRONZE");
        break;        
    default:
        console.log("NO MEDAL");
}

//This is class assignment
// This is simple code for allocation of money based on age using "if else" statement
var age = 10
if (age >= 65){
    console.log("You get your income from your pension")
}else if (age < 65 && age >=18){
    console.log("Each month you get a salary")
}else if (age < 18){
    console.log("You get an allowance")
}else {
    console.log("The value of the age variable is not numerical")
}

//This is simple code for Coding the days of the week program using "switch (case/default)" statement
var day = "wednesday"
switch(day){
    case "monday":
        console.log("Go to Worker")
        break;
    case "tuesday":
        console.log("clean my room")
        break;
    case "wednesday":
        console.log("wash my car");
        break;
    case "thurday":
        console.log("buy grocessories")
        break;
    case "friday":
        console.log("go clubing")
        break;
    case "saturday":
        console.log("do the laundery")
        break;
    case "sunday":
        console.log("go to church")
        break;
    default:
        console.log("There is no such day")                              
}