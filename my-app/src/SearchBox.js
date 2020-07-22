import React, { Component } from 'react';
import './SearchBar.css';

class SearchBox extends Component {
    constructor(props){
        super(props);
        this.state={
            selected: null
        }
        this.handleChange = this.handleChange.bind(this);
        
    }

    handleChange(event){
        this.setState({
          selected: event.target.value
        })
        this.props.action(event.target.value)
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
          return(
              
            <select className="custom-select"
                value={this.state.selected} 
                onChange={this.handleChange}
                 
            >
            {list.map((team) =>(
                <option value={team}>{team}</option>
            ))}
            </select>
          
          )
      }
}

export default SearchBox;