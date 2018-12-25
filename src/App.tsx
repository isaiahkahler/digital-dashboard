import React, { Component } from 'react';
import './App.css';
import styled from 'styled-components';
import { Dash } from './dash';


interface AppProps {}

interface AppState {}

class App extends Component<AppProps, AppState> {
  render() {
    return (
      <div className="App">
        <Dash />
      </div> 
    );
  }

  /* 
    do settings!!
    choose:
      -obd2 specific codes
      -MPH / KMH
  */

}

export default App;
