const MiLB = require('../models/milbModel');

module.exports = class milbController{
    constructor(){}
    listPlayersFromTeam(team){
        return new Promise((resolve, reject)=>{
            MiLB.findAllPlayers((err, dbPlayers)=>{
                if(err) reject(err);
                let dbPlayer = dbPlayers.filter(dbPlayer =>{
                    return dbPlayer.team == team;
                })
                if(dbPlayer.length){
                    resolve(dbPlayer);
                }else{
                    reject("No players found");
                }
            })
        })
    }
}