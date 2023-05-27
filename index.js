const express = require("express");
const data = require("./db");
console.log(data);

const app = express();

app.get("/", (req, res) => {
  res.send("<h1>html</h1>");
});

app.listen(3000);
