var mysqlConn = require("../database");

var Player = function(player){
    this.player_id = player.player_id;
    this.player_name = player.player_name;
    this.team = player.team;
    this.year = player.year;
    this.GS = player.GS;
    this.GP = player.GP;
    this.PA = player.PA;
    this.AB = player.AB;
    this.S = player.S;
    this.D = player.D;
    this.T = player.T;
    this.HR = player.HR;
    this.TB = player.TB;
    this.H = player.H;
    this.R = player.R;
    this.RBI = player.RBI;
    this.SB = player.SB;
    this.CS = player.CS;
    this.BB = player.BB;
    this.IBB = player.IBB;
    this.SO = player.SO;
    this.HBF = player.HBF;
    this.SF = player.SF;
    this.SH = player.SH;
    this.AVG = player.AVG;
    this.OBP = player.OBP;
    this.SLG = player.SLG;
    this.OPS = player.OPS;
    this.wOBA = player.wOBA;
    this.wRAA = player.wRAA;
    this.BF = player.BF;
    this.IP = player.IP;
    this.Ha = player.Ha;
    this.HRa = player.HRa;
    this.TBa = player.TBa;
    this.BBa = player.BBa;
    this.IBBa = player.IBBa;
    this.K = player.K;
    this.HBPa = player.HBPa;
    this.IFFB = player.IFFB;
    this.BK = player.BK;
    this.W = player.W;
    this.L = player.L;
    this.SV = player.SV;
    this.TR = player.TR;
    this.ER = player.ER;
    this.RA = player.RA;
    this.ERA = player.ERA;
    this.FIP = player.FIP;
    this.iFIP = player.iFIP;
    this.FIPR9 = player.FIPR9;
    this.dRPW = player.dRPW;
    this.RAAP9 = player.RAAP9;
    this.WPGAA = player.WPGAA;
    this.WPGAR = player.WPGAR;
    this.WAR = player.WAR;
}
Player.findAllPlayers = function(result){
    mysqlConn.query("SELECT * FROM trade_deadline.Player", function(err, res){
        if(err){
            result(err, null);
        } else{
            result(null, res);
        }
    })
}
Player.findPlayersByTeam = function(team){
    return new Promise((resolve, reject)=>{
        mysqlConn.query("Select * from trade_deadline.Player where team=?", team, (err,res)=>{
            if(err){
                reject(err);
            }else{
                resolve(res);
            }
        })
    })
}

Player.findUniqueNames = function(team){
    return new Promise((resolve, reject) =>{
    mysqlConn.query("SELECT DISTINCT player_name FROM trade_deadline.Player where team=?", team, (err, res)=>{
        if(err){
            reject(err);
        }else{
            resolve(res);
        }
    })
})
}
module.exports = Player;