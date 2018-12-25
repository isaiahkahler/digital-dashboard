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
  rpm: number;
  speed: number;
}

export class Dash extends React.Component<DashProps, DashState> {
  constructor(props: DashProps) {
    super(props);
    this.state = {
      rpm: 0,
      speed: 0
    }
  }

  render() {

    const radius = 200;
    const stroke = 20;
    const progress = 99;

    const normalizedRadius = radius - stroke * 2;
    const circumference = normalizedRadius * 2 * Math.PI;
    const strokeDashoffset = circumference - progress / 100 * circumference;

    return (
      <Container>

        <ProgressRing radius={200} stroke={20} progress={this.state.rpm} color="#ff0000" >
          <ProgressRing radius={200 - 20} stroke={20} progress={this.state.speed} color="#fff" />
        </ProgressRing>

      </Container>
    );
  }
}

const RPMCircleGauge = styled.div`
  width: 50vh;
  height: 50vh;
  border-radius: 25vh;
  background-color: #ff0000;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: 100ms;
`;

const SpeedCircleGauge = styled.div`
  width: 90%;
  height: 90%;
  border-radius: 100%;
  background-color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: 100ms;
`;

// function CircleGauge(props: any) {
//   return (
//     <RPMCircleGauge>
//       <SpeedCircleGauge>
//         <SpeedCircleGauge style={{ backgroundColor: "#000" }}>

//         </SpeedCircleGauge>
//       </SpeedCircleGauge>
//     </RPMCircleGauge>
//   );
// }


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
            stroke-width={stroke}
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