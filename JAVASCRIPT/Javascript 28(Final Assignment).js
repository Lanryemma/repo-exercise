/*//Given variables
const dishData = [
    {
        name: "Italian pasta",
        price: 9.55
    },
    {
        name: "Rice with veggies",
        price: 8.65
    },
    {
        name: "Chicken with potatoes",
        price: 15.55
    },
    {
        name: "Vegetarian Pizza",
        price: 6.45
    },
]
const tax = 1.20;

// Implement getPrices()
function getPrices(taxBoolean) {
    for (var i = 0; i < dishData.length; i++)  {
        var loop = dishData[i]
        var finalPrice;
        if (taxBoolean == true) {
            finalPrice = loop.price + (loop.price*0.20)
        }else if(taxBoolean == false){
            finalPrice = loop.price
        } else {
            console.log("You need to pass a boolean to the getPrices call!")
            console.log('return (to "jump out" of the further function execution)')
        }
        console.log("Dish: ", loop.name, "Price: $", finalPrice);
    } 
}
//getPrices(true)
// Implement getDiscount()
function getDiscount(taxBoolean,guests) {
    getPrices(taxBoolean)
    if (typeof (guests) == 'number' && guests < 30 && guests > 0) {
        var discount = 0;
        if (guests < 5) {
            discount = 5;
        } else if (guests > 5) {
            discount = 10;
        }
        console.log('Discount is: $' + discount);
    } else {
        console.log('The second argument must be a number between 0 and 30')
    }
}

// Call getDiscount()
getDiscount(true, 2)
getDiscount(false, 10)*/

// Given variables
const dishData = [
    {
        name: "Italian pasta",
        price: 9.55
    },
    {
        name: "Rice with veggies",
        price: 8.65
    },
    {
        name: "Chicken with potatoes",
        price: 15.55
    },
    {
        name: "Vegetarian Pizza",
        price: 6.45
    },
]
const tax = 1.20;

// Implement getPrices()
function getPrices(taxBoolean) {
    for (var i = 0; i < dishData.length; i++)  {
        var loop = dishData[i]
        var finalPrice;
        if (taxBoolean === true) {//=== is not neccessary == is fine
            finalPrice = loop.price*tax
        }else if(taxBoolean === false){
            finalPrice = loop.price
        } else {
            console.log("You need to pass a boolean to the getPrices call!")
            return;
        }
        console.log(`Dish: ${loop.name} Price: $${finalPrice}`);
    } 
}

// Implement getDiscount()
function getDiscount(taxBoolean,guests) {
    getPrices(taxBoolean)
    if (typeof (guests) == 'number' && guests < 30 && guests > 0) {
        var discount = 0;
        if (guests < 5) {
            discount = 5;
        } else if (guests > 5) {
            discount = 10;
        }
        console.log(`Discount is: $${discount}`);
    } else {
        console.log('The second argument must be a number between 0 and 30')
    }
}

// Call getDiscount()
getDiscount(true, 2)
getDiscount(false, 10)