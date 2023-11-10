//How do webdevelopers test their rade
//there are javascript testing frame works for testing codes
//such framework include frame works like JEST
//take a look at this example
function concat (one,two){
    return one + two;
} 
//now to make sure the function do exactly what i want 
//i can test it when i call the function
//console.log(concat('abc','def'))//'abcdef'
//console.log(concat(1,2))// i am expecting '12' but i get 3
//now we test using the JEST framework
/*try{
    expect(console.log(concat('abc','def'))).toBe('abcdef')
}catch(err){
    console.log(err.name);
    console.log(err.message)
}*/
test('return one plus two',()=> {
    expect(concat('abc','def')).toBe('abcdef')
})

//the code above will work if you have installed JEST framework


//Types of testing
// three types of testing E2E or into in testing,  
// integration testing and unit testing.

//E2E testing involves opening the website/webapp you created and 
//checking if it works as its suppose to(its the slowest and most expensive testing type)
//type of E2E include(webdriverjs,protractor,cypress)

//Integration testing is testing how parts of your system 
//interact with other parts of your system. In other words, 
//it's testing how separate parts of your apps work together. 
//uses libraries like react js

//unit testing is the cheapest, A unit is the smallest piece 
//of code that you can test separately from the rest of the app
//in Js is usually a function or a method

//Jest also supports code coverage. 
//Code coverage is a measure of what percentage of my code is covered by tests.

//Mocking allows you to separate the code that 
//you are testing from it's related dependencies.
//In other words, you can use the mocking features to 
//make sure that your unit testing is stand-alone.

//Jest allows you to perform snapshot testing.
//used to  verify that there are no regressions in the DOM of 
//our apps after some changes to the code base are made


//TDD (Test-Driven Development)
//Since your coding the TDD way you first write the test, 
//even before you've written any actual implementation
//this example is for testinf if carkey status exist
test('return true if statuskey exists',()=> {
    expect(statuskey).toBeDefined();
})

function statuskey(){}

//now in TDD test, you first write a failing testing(red), the you
//write passing test(green), then you make the final correction to your
//code (this is called 'Refactoring)

/*Prices with 20% tax:
Dish: Italian pasta Price (incl.tax): $ 11.46
Dish: Rice with veggies Price (incl.tax): $ 10.38
Dish: Chicken with potatoes Price (incl.tax): $ 18.66
Dish: Vegetarian Pizza Price (incl.tax): $ 7.74

Prices without tax:
Dish: Italian pasta Price (incl.tax): $ 9.55
Dish: Rice with veggies Price (incl.tax): $ 8.65
Dish: Chicken with potatoes Price (incl.tax): $ 15.55
Dish: Vegetarian Pizza Price (incl.tax): $ 6.458*/