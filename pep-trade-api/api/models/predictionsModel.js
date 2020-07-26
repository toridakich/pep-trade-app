var mysqlConn = require("../database");

var Prediction = function(prediction){
    this.id = prediction.id;
    this.age = prediction.age;
    this.years_remain = prediction.years_remain;
    this.remain_war = prediction.remain_war;
    this.name = prediction.name;
}


Prediction.getAll = function(result){
    mysqlConn.query("SELECT * FROM predictions.predictions", function(err, res){
        if(err){
            result(err, null);
        } else{
            result(null, res);
        }
    })
}

module.exports = Prediction;