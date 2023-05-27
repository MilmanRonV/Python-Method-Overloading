const fs = require("fs");

fs.appendFileSync("./shuman.txt", "testestest");
const data = fs.readFileSync("./shuman.txt", "utf-8");
console.log(data);

module.exports = {
  data,
};
