//When you need your code to perform more than one task at the same time
//you use nested loop(A loop inside another loop)

//in this example we assign week 1 and week 2 to 5days of the week
for (var i = 1; i <=2; i++){
    for (var j = 1; j <=5; j++){
        console.log("Week"+i + " Day"+j)
    }
}

//in this example we dispay the year and the month with nested loop
console.log("year and the month with nested loop")
for (var year = 2023; year < 2026; year++){
    console.log("the year "+ year);
    for (var month = 1; month < 13; month ++){
        console.log("month "+ month)
    }
}
//this is to show the name of the months
console.log('this is to show the name of the months')
for (var year = 2023; year < 2026; year++){
    //console.log("the year "+ year);
    for (var month = 1; month < 13; month ++){
        if (month == 1){
            console.log('January '+ year)
        } else if (month == 2){
            console.log('February '+year)
        }else if (month == 3){
            console.log('March '+ year)
        } else if (month == 4){
            console.log('April ' + year)
        }else if (month == 5){
            console.log('May '+ year)
        } else if (month == 6){
            console.log('June '+ year)
        }else if (month == 7){
            console.log('July '+ year)
        } else if (month == 8){
            console.log('August '+ year)
        }else if (month == 9){
            console.log('September '+ year)
        } else if (month == 10){
            console.log('October '+ year)
        }else if (month == 11){
            console.log('November '+ year) 
        } else if (month == 12){
            console.log('December '+ year)   
        }else {
            console.log(month)
        } 
    }
}

//this is how loops fit into displaying this grid of cards showcasing the letter cubes on sale?
var cubes = 'ABCDEFG';
//styling console output using CSS with a %c format specifier
for (var i = 0; i < cubes.length; i++) {
    var styles = "font-size: 40px; border-radius: 10px; border: 1px solid blue; background: pink; color: purple";
    console.log("%c" + cubes[i], styles)
}
//The cubes.length returns a number. 'ABCDEFG' =  7 letters
//Since cubes is a string of characters the cubes.length gives me the length of the string saved in the variable.
//The second piece of code that's new here is the cubes[i] snippet.
//This simply targets each individual letter in the loop, based on the current value of the i variable.
//In other words, cubes[i], when i is equal to 0, is: A.
//Then, cubes[i], when i is equal to 1, is: B.
//This goes on for as many loops my for loop runs - and this is determined by the cubes.length value.
//It's also very versatile, since, if I, for example, decided to change the length of the cubes string, 
//I would not have to update the condition of i < cubes.length, 
//because it gets automatically updated when I change the length of the cubes string.



//This is class assignment
console.log('This is class assignment using for loop and if-else conditional statement')
//this part involves coding the nested loop using for loop and if-else condition statement
for(var i = 1; i <11; i++){
    if (i == 1){
        console.log('Gold medal')
    } else if (i == 2){
        console.log('Silver medal')
    }else if (i == 3){
        console.log('Bronze medal')
    }else {
        console.log(i)
    }
}
//this part involves coding the nested loop using for loop and switch conditional statement
console.log('This is class assignment using for loop and switch conditional statement')
for(var i = 1; i <11; i++){
   switch (i){
    case 1 :
        console.log('Gold medal')
        break;
    case 2 :
        console.log('Silver medal')
        break;
    case 3 :
        console.log('Bronze medal')
        break;
    default:
        console.log(i)            
   }
}

//this example is from the additional rading example
let name1 = 'alice',
    name2 = 'bob';    

let result = name1 > name2;
console.log(result); // true
console.log(name1 == 'alice'); // true
console.log(10 === '10');