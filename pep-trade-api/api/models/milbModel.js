var mysqlConn = require("../database");

var MiLB = function(milb){
    this.name = milb.name;
    this.score_now = milb.score_now;
    this.score_rebuild = milb.score_rebuild;
    this.predicted_remaining = milb.predicted_remaining;
    this.remain_war = milb.remain_war;
    this.team = milb.team;
}

MiLB.findAllPlayers = function(result){
    mysqlConn.query("SELECT * FROM predictions.milb_batter_preds", function(err, res){
        if(err){
            result(err, null);
        } else{
            result(null, res);
        }
    })
}

module.exports = MiLB;