import React, { Component } from 'react';
import './PlayerInput.css';
import './SearchBar.css';

class PlayerInput extends Component {
    constructor(props){
        super(props);
        this.state={
            name: this.props.name
        }
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(event){
        this.setState({
          name: event.target.value
        })
        this.props.addSelected(event.target.value);
        this.props.update(this.props.identify, event.target.value)
      }



    render(){
        var distinctNames = [...new Set(this.props.players.map(x => x.name))]
        distinctNames.sort();
        let list = distinctNames.map((team) => {
            return (
              <option value={team}>{team}</option>
            )
          })
        
        return(
            
            <div className='pinp'>
                <button type="button" className="del" onClick={()=>this.props.delete(this.state.name, this.props.identify)}>x</button>
            <select className="custom-select"
                id='this'
                value={this.state.name} 
                onChange={this.handleChange}
                placeholder=' '
            >
            
            <option value="none" selected disabled hidden> 
            </option> 
            {list}
            
            </select>
            
            </div>
         )
    }
}

export default PlayerInput;