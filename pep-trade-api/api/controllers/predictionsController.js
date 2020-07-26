const Prediction = require('../models/predictionsModel');

module.exports = class predictionsController{
    constructor(){}

    getPredictionByName(name){
        return new Promise((resolve, reject)=>{
            Prediction.getAll((err, dbPreds)=>{
                if(err) reject(err);
                let dbPred = dbPreds.filter(dbPred =>{
                    return dbPred.name == name;
                })
                if(dbPred.length){
                    resolve(dbPred);
                }else{
                    reject("No prediction found");
                }
            })
        })
    }

}