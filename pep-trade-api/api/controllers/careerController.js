const Career = require('../models/careerModel')

module.exports = class careerController{
    constructor(){}

    getCareerByName(name){
        return new Promise((resolve, reject)=>{
            Career.getAll((err, dbCars)=>{
                if(err) reject(err);
                let dbCar = dbCars.filter(dbCar=>{
                    return dbCar.name == name;
                })
                if(dbCar.length){
                    resolve(dbCar);
                }else{
                    reject("No careers found");
                }
            })
        })
    }

    listPlayersFromTeam(team){
        return new Promise((resolve, reject)=>{
            Career.getAll((err, dbPlayers)=>{
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