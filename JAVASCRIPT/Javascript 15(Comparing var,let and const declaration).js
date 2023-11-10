//WHATS THE DIFFERENCE BETWEEN (var, let or const)
//using the 'let' declaration you cannot:
//* use it before it is declared.
//* redeclare the variable.
//* it is scoped to the block.
//lets give an example of using the 'let' vs the 'var' declaration
console.log(user)
let user = 5;//this will give us error as you can't use a 'let' variable before it is declared. 
//lets do the same thing using the 'var' declaration
console.log(use)
var use = 5;//this will say undefined and not error


//WE SHOW THE REDECLARING DIFFERENCE 
let hot = 100
console.log(hot)
//now we try to redeclare 'hot'
//let hot = 40//this will give us error as we cannot redeclare a 'let' variables
//but we can reassign it
hot = 40;
console.log(hot);

//But using the var declaration
var bot = 100
console.log(bot)
//now we try to redeclare 'bot'
var bot = 45
console.log(bot)


//NOW WE CAN TRY THE 'const declaration'
console.log(us)
const us = 55;//this will give us error as you can't use a 'const' variable before it is declared.
//now we try to redeclare 'us'
const us = 34;//this will give us error as you can't redeclare a 'const' declaration
//but lets try to reassign it
us = 67;
console.log(us)//this will give us error as you can't reassign a 'const' declaration