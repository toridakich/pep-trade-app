const express = require('express');
const router = express.Router();

const MiLBController = require('../controllers/milbController');
const milbController = new MiLBController();

router.post('/getPlayers', (req, res) =>{
    milbController.listPlayersFromTeam(req.body.team)
    .then(players =>{
        res.send(players);
    })
    .catch(err =>{
        res.status(400).json(err);
    })
})

module.exports = router;