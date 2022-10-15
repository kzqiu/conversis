import face from './face.png'; //replace this with an actual image of the heart
import './App.css';
import React from 'react';


function Heart(){
    return(
        <img className="pic" src={face} alt="right-heart"/>
    );
}

export default Heart;