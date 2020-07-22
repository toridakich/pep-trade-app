const express = require('express');
const router = express.Router();

const PlayerController = require('../controllers/playerController');
const playerController = new PlayerController();

router.post('/getPlayers', (req, res) =>{
    playerController.listPlayersFromTeam(req.body.team)
    .then(players =>{
        res.send(players);
    })
    .catch(err =>{
        res.status(400).json(err);
    })
})

router.post('/getUniqueNames', (req, res) =>{
    playerController.listUniqueNames(req.body.team)
    .then(players=>{
        res.send(players)
    })
    .catch(err =>{
        res.status(400).json(err)
    })
})

module.exports = router;