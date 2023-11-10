//to make a function run in an infinite loop you can try it like this
function example(){
    console.log('line 1')
    console.log('line 2')
    console.log('line 3')
    example()
}
//to call the function
//example()

//to make it easier to call a function continously without
//creating an infinite loop we can use recursion function
let counter = 3;
function example1(){
    console.log(counter);
    counter = counter - 1;
    if (counter === 0 ) return;
    example1()
}
//now to call the function
example1()


//SCOPE, HOW SCOPE CHAIN WORK IN JAVASCRIPT
//the scope inside a function is known as local scope
//the scope outside is known as Global 

