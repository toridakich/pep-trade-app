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
                    <div>{Math.floor(stat.remain_war * 100) / 100} WAR</div>
                    <h5>Value until end of year: </h5>
                    <div>{Math.floor(stat.predicted_remaining * 100) / 100} WAR</div>
                    <h5>PEP Score: </h5>
                    <div>Tanking: {Math.floor(stat.score_rebuild * 100) / 100}</div>
                    <div>Win Now: {Math.floor(stat.score_now * 100) / 100}</div>
                {/* {this.props.weight === "tanking" ? <div>{Math.floor(stat.score_rebuild * 100) / 100}</div>: <div>{Math.floor(stat.score_now * 100) / 100}</div>} */}
            </div>

                ))}
                <h4>Total Score: </h4>
                <div className="fin">{Math.floor(this.props.localScore * 100) / 100}</div>
            </div>
        )
    }

}

export default Predictions;