import './App.css';
import React, {useEffect, useState} from 'react';
import axios from 'axios';

function Sentiment (){

    const [sentiment, getSentiment] = useState("")

    useEffect(() => {
        axios
            .get('http://localhost:5000')
            .then(res => {
                const sentiment = res.data;
                console.log(sentiment);
                getSentiment(sentiment);
        }).catch(error => {
            console.log(error)
          })
    })

    return(
        <p>Your sentiment score is: { sentiment }</p>
    )
}
export default Sentiment;