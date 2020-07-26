import React, { Component } from 'react';
import './PlayerInput.css';
import './SearchBar.css';

class PlayerInput extends Component {
    constructor(props){
        super(props);
        this.state={
            name: undefined
        }
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(event){
        this.setState({
          name: event.target.value
        })
        this.props.addSelected(event.target.value);
      }



    render(){
        var distinctNames = [...new Set(this.props.players.map(x => x.name))]
       // if(this.props.playing){
        
        return(
            // <label>
            //         <input
            //         name="player1"
            //         type="text"
            //         value={this.state.name}
            //         onChange={() => this.handleInputChange}
            //         />
            // </label>
            <div className='pinp'>
                <button type="button" className="del" onClick={this.props.delete}>x</button>
            <select className="custom-select"
                id='this'
                value={this.state.name} 
                onChange={this.handleChange}
                 
            >
            
            {distinctNames.map((team) =>(
                <option value={team}>{team}</option>
            ))}
            
            </select>
            
            </div>
         )
    }
}

export default PlayerInput;