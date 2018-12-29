import React, { Component } from 'react';
import './App.css';
import styled from 'styled-components';
import { Dash } from './dash';
import { Socket } from 'net';


interface AppProps {}

interface AppState {
  data: string;
}

class App extends Component<AppProps, AppState> {
  constructor(props: AppProps){
    super(props);
    this.state = {
      data: ''
    }
  }

  render() {
    return (
      <div className="App">
        <Dash />
      </div> 
    );
  }

}

export default App;
