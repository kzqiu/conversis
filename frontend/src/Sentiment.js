import './App.css';
import React from 'react';

const Sentiment = (props) => {
/*
    const [sentiment, getSentiment] = useState("")

    useEffect(() => {
        axios
            .get('http://localhost:5000/sentiment')
            .then(res => {
                const sentiment = res.average;
                console.log(sentiment);
                getSentiment(sentiment);
        }).catch(error => {
            console.log(error)
          })
    })
*/
    return(
        <p>Your sentiment score is: {props.data}</p>
    )
}
export default Sentiment;