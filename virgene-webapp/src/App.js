import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  constructor() {
    super();
    this.state = {
      features: Array(2).fill(null),
    }
    this.state.features[0] = {
      name: "CtrlP",
      description: "Fuzzy file search",
      selected: false,
    }
    this.state.features[1] = {
      name: "Tagbar",
      description: "Tag browser",
      selected: false,
    }
    this.state.features[2] = {
      name: "Disable arrow keys",
      description: "Disable arrow keys, helps you learn to use just hjkl",
      selected: false,
    }
    this.state.features[3] = {
      name: "Highlight search",
      description: "Highlight search results",
      selected: false,
    }
  }
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <h2>Virgene</h2>
          <h3>Extensible, easy to use vimrc generator</h3>
        </div>
        <p className="App-intro">
          Enable and configure Vim features.
        </p>
        <div>
          {this.renderFeature(0)}
          {this.renderFeature(1)}
          {this.renderFeature(2)}
          {this.renderFeature(3)}
        </div>
      </div>
    );
  }
  handleClick(i) {
    const features = this.state.features.slice();
    features[i].selected = !features[i].selected;
    this.setState({features: features});
  }
  renderFeature(i) {
    return <Feature name={this.state.features[i].name} description={this.state.features[i].description} selected={this.state.features[i].selected}  onClick={ () => this.handleClick(i)}/>;
  }
}

function Feature(props) {
  var selectedStyle = {
    background: '#0099ff'
  };
  var regularStyle = {
    background: '#ffffff'
  };
  var dstyle = props.selected ? selectedStyle : regularStyle;
  return (
    <div>
      <button className="square" onClick={() => props.onClick()} style={dstyle}>
        <h1>{props.name}</h1>
        <p>
          {props.description}
        </p>
        <p>
          selected: {props.selected.toString()}
        </p>
      </button>
    </div>
  );
}

export default App;
