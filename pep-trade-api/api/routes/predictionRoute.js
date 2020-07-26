const express = require('express');
const router = express.Router();

const PredictionController = require('../controllers/predictionsController');
const predictionController = new PredictionController();

router.post('/getPrediction', (req, res) =>{
    predictionController.getPredictionByName(req.body.name)
    .then(players =>{
        res.send(players);
    })
    .catch(err =>{
        res.status(400).json(err);
    })
})

module.exports = router;