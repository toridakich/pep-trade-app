import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import SearchBox from './SearchBox';
import PlayerInput from './PlayerInput';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      team1Inputs: ['input-0'],
      team2Inputs: ['input-0'],
      team1Players: [],
      team2Players: [],
      team1: 'ANA',
      team2: 'ANA'

    }
    this.addPlayer1 = this.addPlayer1.bind(this);
    this.addPlayer2 = this.addPlayer2.bind(this);
    this.getTeam1 = this.getTeam1.bind(this);
    this.getTeam2 = this.getTeam2.bind(this);
  }




  addPlayer1() {
    var newInput = `input-${this.state.team1Inputs.length}`;
    this.setState(prevState => ({ team1Inputs: prevState.team1Inputs.concat(newInput) }));
  }

  addPlayer2() {
    var newInput = `input-${this.state.team2Inputs.length}`;
    this.setState(prevState => ({ team2Inputs: prevState.team2Inputs.concat(newInput) }));
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

  componentDidUpdate(_, prevState) {
    let currentComponent = this;
    const team1 = {
      "team": currentComponent.state.team1
    }
    console.log({a: team1.team, b: prevState.team1});
    if(team1.team != prevState.team1){
      console.log('fetching')
    fetch('http://localhost:4000/api/player/getPlayers', {
      method: 'post',
      body: JSON.stringify(
        team1
      ),
      headers: { "Content-Type": "application/json" }
    })
      .then(res => res.json())
      .then(function (res) {
        if(res != "No players found"){
        
        currentComponent.setState({
          team1Players: res
        })
      }

      });
    }
    const team2 = {
      "team": currentComponent.state.team2
    }
    if(team2.team != prevState.team2){
    fetch('http://localhost:4000/api/player/getPlayers', {
      method: 'post',
      body: JSON.stringify(
        team2
      ),
      headers: { "Content-Type": "application/json" }
    })
      .then(res => res.json())
      .then(function (res) {
        if(res != 'No players found'){
        currentComponent.setState({
          team2Players: res
        })
      }
      });
    }

  }

  render() {
    console.log(this.state.team2)
    return (
      <div className="App">

        <div className="teamBars">
          <p>Team 1:</p>
          <SearchBox action={this.getTeam1} />
          <p>Players:</p>
          <div className="dynamicInput">
            {this.state.team1Inputs.map(team1Input =>
              <div id="individies">
                <PlayerInput key={team1Input} players={this.state.team1Players}/>
              </div>)}
          </div>
          <div className='add'>
            <button type='button' onClick={this.addPlayer1}>Add Player</button>
          </div>
        </div>
        <div className="t2">
          <p>Team 2:</p>
          <SearchBox action={this.getTeam2} />
          <p>Players:</p>
          <div className="dynamicInput">
            {this.state.team2Inputs.map(team2Input =>
              <div id='individies'>
                <PlayerInput key={team2Input} players={this.state.team2Players}/>
              </div>)}
          </div>
          <div className='add'>
            <button type='button' onClick={this.addPlayer2}>Add Player</button>
          </div>

        </div>
        <div className="submit">
          <button type='button'>submit</button>
        </div>
      </div>
    );
  }
}

export default App;
