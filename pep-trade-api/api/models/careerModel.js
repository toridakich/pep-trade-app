var mysqlConn = require("../database");

var Career = function(career){
    this.name = career.name;
    this.score_now = career.score_now;
    this.score_rebuild = career.score_rebuild;
    this.predicted_remaining = career.predicted_remaining;
    this.remain_war = career.remain_war;
    this.team = career.team;
    
}

Career.getAll = function(result){
    mysqlConn.query("SELECT * FROM predictions.final", function(err, res){
        if(err){
            result(err, null);
        } else{
            result(null, res);
        }
    })
}

module.exports = Career;