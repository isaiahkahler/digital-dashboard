import * as React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  width: 100vw;
  height: 100vh;
  background-color: #000;
  color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const CenterText = styled.div`
  text-align: center;
`;


interface DashProps { }
interface DashState {
  rpm: number,
  speed: number,
}

export class Dash extends React.Component<DashProps, DashState> {
  constructor(props: DashProps) {
    super(props);
    this.state = {
      rpm: 0,
      speed: 0
    }
  }

  componentDidMount = () => {
    this.setState({
      rpm: 22,
      speed: 0
    })

    setTimeout(() => {
      this.setState({
        rpm: 25,
        speed: 75
      })
    }, 1000)
    setTimeout(() => {
      this.setState({
        rpm: 0,
        speed: 25
      })
    }, 2000)
    setTimeout(() => {
      this.setState({
        rpm: 99,
        speed: 0
      })
    }, 3000)
    setTimeout(() => {
      this.setState({
        rpm: 78,
        speed: 125
      })
    }, 5000)

  }

  render() {

    // const width = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
    const height = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);

    return (
      <Container>

        <ProgressRing radius={(height / 3)} stroke={20} progress={this.state.rpm} color="#ff0000" >
          <ProgressRing radius={(height / 3) - 20} stroke={20} progress={this.state.speed} color="#fff" >
            <CenterText>
              <h1>{Math.round(this.state.speed)}</h1>
              <h2>MPH</h2>
            </CenterText>
          </ProgressRing>
        </ProgressRing>

      </Container>
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
        </svg>
        <div style={{ position: "absolute" }}>
          {this.props.children}
        </div>
      </div>
    );
  }
}