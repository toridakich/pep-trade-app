const Player = require('../models/playerModel');

module.exports = class playerController{
    constructor(){}

    listPlayersFromTeam(team){
        return new Promise((resolve, reject)=>{
            Player.findAllPlayers((err, dbPlayers)=>{
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

    listUniqueNames(team){
        return new Promise((resolve, reject)=>{
            Player.findUniqueNames(team, (err, res) =>{
                if(err){
                    reject(err)
                }
                resolve(res);
            })
        })
    }
}