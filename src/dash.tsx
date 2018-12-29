import * as React from 'react';
import styled from 'styled-components';
import moment from 'moment';
import { OilTemperature, Gas, Alert, ChevRight, Camera } from './icons';

const TopContainer = styled.div`
  width: 100vw;
  height: 100vh;
  position: absolute;
  z-index: 2;
  color: #fff;
  display: flex;
  justify-content: center;
  align-items: center; 
`;

const Container = styled.div`
  width: 100vw;
  height: 100vh;
  color: #fff;
  background-color: #000;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
`;

const Column = styled.div`
  padding: 0px 5vh;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
`;

const CenterColumn = styled.div`
  width: 50vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
`;

const VerticalGauge = styled.div`
  height: 40vh;
  width: 5vw;
  border: 3px solid #fff;
  display: flex;
  flex-direction: column-reverse;
`;

const IconContainer = styled.div`
  width: inherit;
  height: inherit;
  position: absolute;
  z-index: 2;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const CenterText = styled.div`
  text-align: center;
`;

const MessagesContainer = styled.div`
  margin: 5vh 0px;
`;


interface DashProps { }
interface DashState {
  time: string,
  rpm: number,
  speed: number,
  gas: number,
  temp: number,
  messages: string[]
}

export class Dash extends React.Component<DashProps, DashState> {
  socket: WebSocket | undefined;

  constructor(props: DashProps) {
    super(props);
    this.socket = new WebSocket('ws://localhost:3001');
    this.state = {
      time: moment().format("LT"),
      rpm: 0,
      speed: 0,
      gas: 0,
      temp: 0,
      messages: []
    }
  }


  componentDidMount() {
    const socket = this.socket;
    if (!socket) return;
    socket.addEventListener('open', () => {
      socket.send('hi');
      socket.addEventListener('message', (msg) => {
        const data = JSON.parse(msg.data);
        this.setState({ ...data });
      })
    })
    this.updateTime();
  }

  updateTime = () => {
    this.setState({
      time: moment().format("LT")
    })
    setTimeout(() => this.updateTime(), 10000)
  }

  handleCameraClick () {
    this.socket && this.socket.send(JSON.stringify({'show-camera': true}))
  }

  render() {

    // const width = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
    const height = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);

    return (
      <div>

        <TopContainer>
          <ProgressRing radius={(height / 3)} stroke={20} progress={this.state.rpm} color="#ff0000" >
            <ProgressRing radius={(height / 3) - 20} stroke={20} progress={this.state.speed} color="#1e7cff" >
              <CenterText>
                <h1>{this.state.speed}</h1>
                <h3>MPH</h3>
              </CenterText>
            </ProgressRing>
          </ProgressRing>
        </TopContainer>

        <Container>
          <Column>
            <div style={{
              width: '8vw',
              height: '8vw',
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}>
              <div onClick={() => this.handleCameraClick()}>
                <Camera />
              </div>
            </div>
          </Column>
          <CenterColumn>
            <h2 style={{ margin: "5vh 0px" }}>{this.state.time}</h2>
            <MessagesContainer>
              {this.state.messages.map((item, index) => {
                return (<div key={index}>
                  <Alert style={{ display: "inline", verticalAlign: "middle" }} />
                  <h3 style={{ display: "inline", verticalAlign: "middle" }}>{item}</h3>
                </div>)
              })}
            </MessagesContainer>
          </CenterColumn>
          <Column>
            <VerticalGauge style={{ backgroundImage: "linear-gradient(red, blue)", flexDirection: "column" }}>
              <IconContainer>
                <OilTemperature />
              </IconContainer>
              <div style={{ width: "100%", height: (100 - this.state.temp) + "%", backgroundColor: "#000", transition: "250ms" }} />
            </VerticalGauge>
            <VerticalGauge>
              <IconContainer>
                <Gas />
              </IconContainer>
              <div style={{ width: "100%", height: this.state.gas + "%", backgroundColor: "#23D160", transition: "250ms" }} />
            </VerticalGauge>
          </Column>
        </Container>

      </div>
    );
  }
}


interface ProgressRingProps {
  radius: number,
  stroke: number,
  progress: number,
  color: string,
  children?: React.ReactChild
}
interface ProgressRingState {
  normalizedRadius: number,
  circumference: number
}

class ProgressRing extends React.Component<ProgressRingProps, ProgressRingState> {
  constructor(props: ProgressRingProps) {
    super(props);
    const radius = props.radius;
    const stroke = props.stroke;
    this.state = {
      normalizedRadius: radius - stroke * 2,
      circumference: (radius - stroke * 2) * 2 * Math.PI
    }

  }

  render() {
    const { radius, stroke, progress } = this.props;
    const strokeDashoffset = this.state.circumference - progress / 100 * this.state.circumference;

    return (
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center" }}>
        <svg
          height={radius * 2}
          width={radius * 2}
          transform='rotate(90)'
        >
          <circle
            id="progress-circle"
            stroke={this.props.color}
            fill="transparent"
            strokeWidth={stroke}
            strokeDasharray={this.state.circumference + ' ' + this.state.circumference}
            style={{ strokeDashoffset, transition: "250ms" }}
            r={this.state.normalizedRadius}
            cx={radius}
            cy={radius}
          />
          <circle
            id="progress-circle"
            stroke={this.props.color}
            fill="transparent"
            strokeWidth={3}
            r={this.state.normalizedRadius + (stroke / 2)}
            cx={radius}
            cy={radius}
          />
        </svg>
        <div style={{ position: "absolute" }}>
          {this.props.children}
        </div>
      </div>
    );
  }
}