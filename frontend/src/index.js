import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Audio from './Audio';
import Heart from './Heart';
import Sentiment from './Sentiment';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <div className="App">
      <div className="App-header">
        <h1 className="cursive">Can I hear your love tonight??? ;))</h1>
        <React.StrictMode>
          <div className="container">
            <Heart/>
            <Heart/>
          </div>
          <Sentiment/>
          <Audio/>
        </React.StrictMode>
      </div>
    </div>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
