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


interface DashProps { }
interface DashState {
  width: number,
  height: number,
  rpm: number;
  speed: number;
}

export class Dash extends React.Component<DashProps, DashState> {
  constructor(props: DashProps) {
    super(props);
    this.state = {
      width: Math.max(document.documentElement.clientWidth, window.innerWidth || 0),
      height: Math.max(document.documentElement.clientHeight, window.innerHeight || 0),
      rpm: 0,
      speed: 0
    }
  }

  handleResize = () => {
    console.log("resize")
    this.setState({
      width: Math.max(document.documentElement.clientWidth, window.innerWidth || 0),
      height: Math.max(document.documentElement.clientHeight, window.innerHeight || 0)
    })
  }

  componentDidMount() {
    this.setState({
      rpm: 22,
      speed: 82
    })

    window.addEventListener('resize', this.handleResize, {passive: true})
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.handleResize);
  }


  render() {

    return (
      <Container>

        <ProgressRing radius={(this.state.height / 4)} stroke={20} progress={this.state.rpm} color="#ff0000" >
          <ProgressRing radius={(this.state.height / 4) - 20} stroke={20} progress={this.state.speed} color="#fff" />
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
            stroke={this.props.color}
            fill="transparent"
            strokeWidth={stroke}
            strokeDasharray={this.state.circumference + ' ' + this.state.circumference}
            style={{ strokeDashoffset }}
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