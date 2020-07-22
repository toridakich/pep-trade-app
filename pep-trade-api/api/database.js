"use strict";

const mysql = require("mysql");

const config = {
  host: "35.245.199.134",
  port: 3306,
  user: "toridakich",
  database: "retrosheet"
};

var connection = mysql.createConnection(config);
connection.connect(err => {
  if (err){
    console.log(err);
  } else{
    console.log("Database Connected: " + config.host + ":" + config.port);
  }
  
});

module.exports = connection;