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
  socket: WebSocket | undefined;
  
  constructor(props: AppProps){
    super(props);
    this.socket = new WebSocket('ws://localhost:3001');
    this.state = {
      data: ''
    }
  }

  componentDidMount = () => {
    this.socket && this.socket.addEventListener('open', () => {
      this.socket && this.socket.addEventListener('message', (msg) => {
        this.setState({data: msg.data})
      })
    })
  }

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
