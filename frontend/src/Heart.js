import heart from './logo.svg'; //replace this with an actual image of the heart
import './App.css';
import React from 'react';

console.log(heart);

function Heart(){
    return(
        <img className="pic" src={heart} alt="right-heart"/>
    );
}

export default Heart;