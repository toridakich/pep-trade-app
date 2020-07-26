const express = require('express');
const router = express.Router();

const CareerController = require('../controllers/careerController');
const careerController = new CareerController();

router.post('/getCareer', (req, res) =>{
    careerController.getCareerByName(req.body.name)
    .then(players =>{
        res.send(players);
    })
    .catch(err =>{
        res.status(400).json(err);
    })
})

router.post('/getPlayers', (req, res) =>{
    careerController.listPlayersFromTeam(req.body.team)
    .then(players =>{
        res.send(players);
    })
    .catch(err =>{
        res.status(400).json(err);
    })
})

module.exports = router;