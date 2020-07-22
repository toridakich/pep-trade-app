const express = require('express');
const logger = require('./api/utilities/logger');
const app = express();
const playerRoute = require('./api/routes/playerRoute');
var cors = require("cors");

app.use(logger);

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use('/api/player', playerRoute);

const port = process.env.PORT || 4000;

app.listen(port);

console.log('todo list RESTful API server started on: ' + port);