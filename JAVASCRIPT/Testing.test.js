// first import the exported add function 
//const{ default: TestRunner } = require("jest-runner")
const Testing = require(`./Testing`);
test('returns the number plus 5',()=>{
    expect(Testing(1)).toBe(6);
})