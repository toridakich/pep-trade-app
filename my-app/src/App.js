import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import SearchBox from './SearchBox';
import PlayerInput from './PlayerInput';
import Predictions from './Predictions';



class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      team1Inputs: ['input-0'],
      team2Inputs: ['input-0'],
      team1Players: [''],
      team2Players: [''],
      team1: 'ANA',
      team2: 'ANA',
      showPop: null,
      selectedTeam1Players: [],
      selectedTeam2Players: [],
      team1Score: 0,
      team2Score: 0,
      team1Weight: 'tanking',
      team2Weight: 'tanking',
      team1Discrep: 0,
      team2Discrep: 0,
      message: "Trade is unfair",
      player1Data: [],
      player2Data:[],
      localScore1: 0,
      localScore2: 0

    }
    this.addPlayer1 = this.addPlayer1.bind(this);
    this.addPlayer2 = this.addPlayer2.bind(this);
    this.getTeam1 = this.getTeam1.bind(this);
    this.getTeam2 = this.getTeam2.bind(this);
    this.removePlayer1 = this.removePlayer1.bind(this);
    this.removePlayer2 = this.removePlayer2.bind(this);
    this.showPop = this.showPop.bind(this);
    this.addSelectedPlayer1 = this.addSelectedPlayer1.bind(this);
    this.addSelectedPlayer2 = this.addSelectedPlayer2.bind(this);
    this.change1Weight = this.change1Weight.bind(this);
    this.change2Weight = this.change2Weight.bind(this);
    this.change1Score = this.change1Score.bind(this);
    this.change2Score = this.change2Score.bind(this);
    this.getDiscreps = this.getDiscreps.bind(this);
    this.setPlayer1Data = this.setPlayer1Data.bind(this);
    this.setPlayer2Data = this.setPlayer2Data.bind(this);
    this.clearList1 = this.clearList1.bind(this);
    this.clearList2 = this.clearList2.bind(this);
    this.clearInput1 = this.clearInput1.bind(this);
    this.clearInput2 = this.clearInput2.bind(this);
    this.updateList1 = this.updateList1.bind(this);
    this.updateList2 = this.updateList2.bind(this);
  }
  updateList1(index, name){
   let players = [...this.state.selectedTeam1Players];
   
   players[index] = name;
   this.setState({
     selectedTeam1Players: players
   })
  }
  updateList2(index, name){
    let players = [...this.state.selectedTeam2Players];
    
    players[index] = name;
    this.setState({
      selectedTeam2Players: players
    })
   }

  clearList1(){
    this.setState({
      selectedTeam1Players: [],
      team1Score: 0,
      player1Data: [],
      localScore1: 0,
      team1Discrep: 0,
      
    })
  }

  clearList2(){
    this.setState({
      selectedTeam2Players: [],
      team2Score: 0,
      player2Data: [],
      localScore2: 0,
      team2Discrep: 0,
    })
  }

  clearInput1(){
    this.setState({
      team1Inputs: ['input-0'],
      team1MInput: ['input-0']
    })
  }

  clearInput2(){
    this.setState({
      team2Inputs: ['input-0']
    })
  }

  setPlayer1Data(data){
    this.setState({
      player1Data: this.state.player1Data.concat(data)
    })
  }

  setPlayer2Data(data){
    this.setState({
      player2Data: this.state.player2Data.concat(data)
    })
  }

  getDiscreps() {
    var t1s = this.state.team1Score - this.state.team2Score;
    var t2s = t1s * (-1);
    this.setState({
      team1Discrep: t1s,
      team2Discrep: t2s
    })
  }
  change1Score(score) {
    this.setState({
      team1Score: score
    })
  }

  change2Score(score) {
    this.setState({
      team2Score: score
    })
  }

  change1Weight(weight) {
    console.log(weight)
    this.setState({
      team1Weight: weight
    })
  }

  change2Weight(weight) {
    this.setState({
      team2Weight: weight
    })
  }

  addSelectedPlayer1(player) {
    this.setState(prevState => ({ selectedTeam1Players: prevState.selectedTeam1Players.concat(player) }))
  }
  addSelectedPlayer2(player) {
    this.setState(prevState => ({ selectedTeam2Players: prevState.selectedTeam2Players.concat(player) }))
  }

  addPlayer1() {
    var newInput = `input-${this.state.team1Inputs.length}`;
    this.setState(prevState => ({ team1Inputs: prevState.team1Inputs.concat(newInput) }));
  }

  addPlayer2() {
    var newInput = `input-${this.state.team2Inputs.length}`;
    this.setState(prevState => ({ team2Inputs: prevState.team2Inputs.concat(newInput) }));
  }

  removePlayer1(name, index) {
    console.log(index);
    this.setState({
      team1Inputs: this.state.team1Inputs.filter((_, i) => i !== index),
      selectedTeam1Players: this.state.selectedTeam1Players.filter(function(player){
        console.log(player);
        return player !== name
      })
    });
    
    
  } 

  removePlayer2(name, index) {

    this.setState({
      team2Inputs: this.state.team2Inputs.filter((_, i) => i !== index),
      selectedTeam2Players: this.state.selectedTeam2Players.filter(function(player){
        console.log(player);
        return player !== name
      })
    });
  }

  getTeam1(team) {

    this.setState({
      team1: team
    })
  }

  getTeam2(team) {
    this.setState({
      team2: team
    })
  }

  showPop(t1, t2) {
    return (
      <div className="popup">
        <div className="main">
          <div className="teamOne">
            <h2>{this.state.team1} players</h2>
            <Predictions players={this.state.selectedTeam1Players} weight={this.state.team1Weight} changeScore={this.change1Score} setPlayer={this.setPlayer1Data} localScore={this.state.localScore1}/>
          </div>
          <div className="teamTwo">
            <h2>{this.state.team2} players</h2>
            <Predictions players={this.state.selectedTeam2Players} weight={this.state.team2Weight} changeScore={this.change2Score} setPlayer={this.setPlayer2Data} localScore={this.state.localScore2}/>
          </div>
        </div><br></br>
       
        <button type="button" className="close" onClick={() => this.setState({ showPop: null })}>x</button>
      </div>
    )
  }
  componentDidMount() {
    let currentComponent = this;
    const team1 = {
      "team": currentComponent.state.team1
    }


    fetch('http://localhost:4000/api/career/getPlayers', {
      method: 'post',
      body: JSON.stringify(
        team1
      ),
      headers: { "Content-Type": "application/json" }
    })
      .then(res => res.json())
      .then(function (res) {
        if (res != "No players found") {

          currentComponent.setState({
            team1Players: res
          })
        }

      });
      

    const team2 = {
      "team": currentComponent.state.team2
    }

    fetch('http://localhost:4000/api/career/getPlayers', {
      method: 'post',
      body: JSON.stringify(
        team2
      ),
      headers: { "Content-Type": "application/json" }
    })
      .then(res => res.json())
      .then(function (res) {
        if (res != 'No players found') {
          currentComponent.setState({
            team2Players: res
          })
        }
      });


  }


  componentDidUpdate(_, prevState) {
    let currentComponent = this;
    const team1 = {
      "team": currentComponent.state.team1
    }
    console.log(currentComponent.state.team1Players);
    if (team1.team != prevState.team1) {
      console.log('fetching')
      fetch('http://localhost:4000/api/career/getPlayers', {
        method: 'post',
        body: JSON.stringify(
          team1
        ),
        headers: { "Content-Type": "application/json" }
      })
        .then(res => res.json())
        .then(function (res) {
          if (res != "No players found") {

            currentComponent.setState({
              team1Players: res
            })
          }

        });

      
    }
    const team2 = {
      "team": currentComponent.state.team2
    }
    if (team2.team != prevState.team2) {
      fetch('http://localhost:4000/api/career/getPlayers', {
        method: 'post',
        body: JSON.stringify(
          team2
        ),
        headers: { "Content-Type": "application/json" }
      })
        .then(res => res.json())
        .then(function (res) {
          if (res != 'No players found') {
            currentComponent.setState({
              team2Players: res
            })
          }
        });

    }
    
    if(currentComponent.state.player2Data != prevState.player2Data || currentComponent.state.player1Data != prevState.player1Data || currentComponent.state.showPop != prevState.showPop){
      var score1 = 0;
      console.log(this.state.team1Weight)
      if(currentComponent.state.team1Weight === "tanking"){
       
        for(var i=0; i < this.state.player1Data.length; i++){
            
            score1 = score1 - this.state.player1Data[i].score_rebuild
        }
        for(var k=0; k<this.state.player2Data.length; ++k){
          score1 = score1 + this.state.player2Data[k].score_rebuild
        }
    } else{
        for(var j=0; j < this.state.player1Data.length; j++){
            
            score1 = score1 - this.state.player1Data[j].score_now;
        }
        for(var l=0; l<this.state.player2Data.length; ++l){
          score1 = score1 + this.state.player2Data[l].score_now;
        }
    }
    var score2=0
    if(currentComponent.state.team2Weight === "tanking" && this.state.player1Data != undefined && this.state.player2Data != undefined){
      
      for(var i=0; i < this.state.player2Data.length; i++){
          
          score2 = score2 - this.state.player2Data[i].score_rebuild
      }
      for(var k=0; k<this.state.player1Data.length; ++k){
        score2 = score2 + this.state.player1Data[k].score_rebuild
      }
  } else{
      for(var j=0; j < this.state.player2Data.length; j++){
          
          score2 = score2 - this.state.player2Data[j].score_now;
      }
      for(var l=0; l<this.state.player1Data.length; ++l){
        score2 = score2 + this.state.player1Data[l].score_now;
      }
  }
    this.setState({
      localScore1: score1,
      localScore2: score2
    })
    if (score1 <= 0.9 && score1 >= -0.9) {
      console.log('in here');
      currentComponent.setState({
        message: "Trade is fair"
      })
    }
    
    }
    if (currentComponent.state.team1Score!= prevState.team1Score|| currentComponent.state.team2Score != prevState.team2Score) {
      var t1s = currentComponent.state.team1Score - currentComponent.state.team2Score;
      var t2s = currentComponent.state.team2Score - currentComponent.state.team1Score;
      currentComponent.setState({
        team1Discrep: t1s*(-1),
        team2Discrep: t2s*(-1)
      })
      if (t1s <= 0.9 && t1s >= -0.9) {
        console.log('in here');
        currentComponent.setState({
          message: "Trade is fair"
        })
      }
    }

  }

  render() {
    console.log(this.state.selectedTeam1Players)
    console.log(this.state.team1Inputs)
    
    return (
      <div className="App">

        <div className="teamBars">
          <h1>Team 1:</h1>
          
          <SearchBox action={this.getTeam1} changeWeight={this.change1Weight} clearList={this.clearList1} clearInput={this.clearInput1}/>
          <p>Players:</p>
          <div className="dynamicInput">
            {this.state.team1Inputs.map((team1Input, index) =>
              <div id="individies">
                <PlayerInput key={team1Input} identify={index} players={this.state.team1Players} delete={this.removePlayer1} addSelected={this.addSelectedPlayer1} name={this.state.selectedTeam1Players[index]} update={this.updateList1}/>
              </div>)}
          </div>
          <div className='add'>
            <button type='button' onClick={this.addPlayer1}>Add Player</button>
          </div>

        </div>

        <div className="t2">
          <h1>Team 2:</h1>
    
          <SearchBox action={this.getTeam2} changeWeight={this.change2Weight} clearList={this.clearList2} clearInput={this.clearInput2}/>
          <p>Players:</p>
          <div className="dynamicInput">
            {this.state.team2Inputs.map((team2Input, index) =>
              
              <div id='individies'>
                
                <PlayerInput key={team2Input} identify={index} players={this.state.team2Players} delete={this.removePlayer2} addSelected={this.addSelectedPlayer2} name={this.state.selectedTeam2Players[index]} update={this.updateList2}/>
              </div>)}
          </div>
          <div className='add'>
            <button type='button' onClick={this.addPlayer2}>Add Player</button>
          </div>
          

        </div>
        <div className="submit">
          <button type='button' onClick={() => this.setState({ showPop: this.state.team1 })}>Submit</button>
        </div>
        {this.state.showPop === this.state.team1 ? this.showPop(this.state.team1) : null}
      </div>
    );
  }
}

export default App;
