import React, {Component} from 'react';
import './Predictions.css'

class Predictions extends Component{
    constructor(props){
        super(props);
        this.state = {
            eachPlayer: []
            
        }
        this.getStats = this.getStats.bind(this);
        //this.findScore = this.findScore.bind(this);
    }
    getStats(name){
        let currentComponent = this;
        const person = {
            'name': name
        }
        fetch('http://localhost:4000/api/career/getCareer', {
            method: 'post',
            body: JSON.stringify(
                person
            ),
            headers: {"Content-Type": "application/json"}
        })
        .then(res => res.json())
        .then(function(res){
            currentComponent.setState({
                eachPlayer: currentComponent.state.eachPlayer.concat(res)
            })
            currentComponent.props.setPlayer(res);
            
        })
    }
    componentDidMount(){
        
        for(var i=0; i< this.props.players.length; i++){
            this.getStats(this.props.players[i]);
        }
        
    }

    componentDidUpdate(_, prevState){
    //     var score = 0;
    //     console.log(this.props.weight)
    //     if(this.state.eachPlayer != prevState.eachPlayer){
    //     if(this.props.weight === "tanking"){
    //         console.log(this.state.eachPlayer.length)
    //         for(var i=0; i < this.state.eachPlayer.length; i++){
                
    //             score = score + this.state.eachPlayer[i].score_rebuild
    //         }
    //     } else{
    //         for(var j=0; j < this.state.eachPlayer.length; j++){
                
    //             score = score + this.state.eachPlayer[j].score_now;
    //         }
    //     }
        
    //     this.props.changeScore(score);
    //     console.log(score);
    //     this.setState({
    //         localScore: score
    //     })
    // }
    }

    
    render(){
        
        
        console.log(this.state.eachPlayer)
        return(
            <div className="stats">
                
                {this.state.eachPlayer.map((stat, key) =>(
                    <div key={key}>
                        <h3>{stat.name}</h3>
                    <h5>Value left on contract: </h5>
                    <div>{stat.remain_war}</div>
                    <h5>Value until end of year: </h5>
                    <div>{stat.predicted_remaining}</div>
                    <h5>Score: </h5>
                {this.props.weight === "tanking" ? <div>{stat.score_rebuild}</div>: <div>{stat.score_now}</div>}
            </div>

                ))}
                <h4>Total Score: </h4>
                <div>{this.props.localScore}</div>
            </div>
        )
    }

}

export default Predictions;