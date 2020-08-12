import React, { Component } from 'react';
import './SearchBar.css';

class SearchBox extends Component {
    constructor(props){
        super(props);
        this.state={
            selected: null,
            weight: "tanking"
        }
        this.handleChange = this.handleChange.bind(this);
        this.handleChangeWeight = this.handleChangeWeight.bind(this);
    }

    handleChange(event){
        this.setState({
          selected: event.target.value
        })
        this.props.action(event.target.value);
        this.props.clearList();
        this.props.clearInput();
      }

      handleChangeWeight(event){
        this.setState({
          weight: event.target.value
        })
        this.props.changeWeight(event.target.value)
      }

      toggleList(){
        this.setState(prevState => ({
          listOpen: !prevState.listOpen
        }))
      }



      render(){
          const list = ['ANA',
          'ARI',
          'ATL',
          'BAL',
          'BOS', 'CHA',
          'CHN',
          'CIN',
          'CLE',
          'COL', 'DET',
          'FLO',
          'HOU',
          'KCA',
          'LAN', 'MIA',
          'MIL',
          'MIN',
          'NYA',
          'NYN', 'OAK',
          'PHI',
          'PIT',
          'SDN',
          'SEA', 'SFN',
          'STL',
          'TBA',
          'TEX',
          'TOR',
          'WAS'];
          const weights = ['tanking', 'win now']
          return(
             <div>
            <select className="custom-select"
                id= "teamSearch"
                value={this.state.selected} 
                onChange={this.handleChange}
                 
            >
            {list.map((team) =>(
                <option value={team}>{team}</option>
            ))}
            </select><br></br>
              <select className="custom-select"
              value={this.state.weight} 
              onChange={this.handleChangeWeight}
              
          >
          {weights.map((team) =>(
              <option value={team}>{team}</option>
          ))}
          
      </select>
      
      </div> 
          )
      }
}

export default SearchBox;