//Moving data around on the web
//a data interchange format based on JavaScript objects
// this format was JSON, which is JavaScript Object Notation
//the two major reasons for the JSON format becoming 
//the dominant data interchange format
/* []it's very lightweight, with syntax very similar to "a stringified JavaScript object"
   []it's easier to handle in JavaScript code, since, JSON, after all, is just JavaScript.*/
//For example, if you had a website with the data on stock price movements
//if the stringified JSON data was converted to an object that had the following structure:
const currencyInfo = {
    //[
        USD: {
            // ...
        },
        GBP: {
            // ...
        },
        EUR: {
            // ...
        }
   // ]
}

//Only a subset of values in JavaScript can be properly stringified to JSON
/*These values include:

* primitive values: strings, numbers, bolleans, null

* complex values: objects and arrays (no functions!)

* Objects have double-quoted strings for all keys

* Properties are comma-delimited both in JSON objects and in JSON arrays, just like in regular JavaScript code

* String properties must be surrounded in double quotes. For example:
  "fruits",
  "vegetables"

* Number properties are represented using the regular JavaScript number syntax; e.g
  5,
  10,
  1.2

* Boolean properties are represented using the regular JavaScript boolean syntax, that is:
  true
  and
  false

* Null as a property is the same as in regular JavaScript; it's just a
  null */


//Some examples of JSON strings
'{"color":"red", "nestedObject": { "color": "blue" } }' 
//It's also possible to have a JSON string encoding just like an array:
'["one", "two", "three"]'
//Obviously, just like objects, 
//arrays can nest other simple or complex data structures
'[{ "color": "blue" }, {"color: "red"}]'


// So to work with JSON, it is common to convert it back to 
//a JavaScript object to work with its properties and methods
'{"greetings":"Hello"}'
const jstr = '{"greetings":"Hello"}';
JSON.parse(jstr)//{greetings: 'Hello'}
//now we can change the value of 'hello'
const change = JSON.parse(jstr);
change.greetings = 'hola'
console.log(change)

//NOW TO CONVERT JAVASCRIPT OBJECT TO JSON SYNTHAX
const obj = {
  first: 'look',
  second: 'at',
  third: 'this',
  fouth: 'fool'
}
JSON.stringify(obj)
const see = JSON.stringify(obj)
console.log(see)

