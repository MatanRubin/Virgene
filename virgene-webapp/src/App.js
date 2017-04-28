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
      visible: true,
    }
    this.state.features[1] = {
      name: "Tagbar",
      description: "Tag browser",
      selected: false,
      visible: true,
    }
    this.state.features[2] = {
      name: "Disable arrow keys",
      description: "Disable arrow keys, helps you learn to use just hjkl",
      selected: false,
      visible: true,
    }
    this.state.features[3] = {
      name: "Highlight search",
      description: "Highlight search results",
      selected: false,
      visible: true,
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
        <div className="features-config">
          <FeaturesNavigator features={this.state.features} onClickNav={(i) => this.handleClick(i)} onSearch={(searchString) => this.handleSearch(searchString)}/>
          <FeatureDetails features={this.state.features} />
        </div>
      </div>
    );
  }

  handleClick(i) {
    const features = this.state.features.slice();
    features.forEach((feature) => feature.selected = false);
    features[i].selected = true;
    this.setState({features: features});
  }

  handleSearch(searchString) {
    const features = this.state.features.slice();
    features.forEach((feature) => feature.visible = feature.name.toLowerCase().includes(searchString.toLowerCase()));
    this.setState({features: features});
  }
}

function FeatureDetails(props) {
  var selectedFeatures = props.features.filter(function(feature) {
    return feature.selected;
  });
  if (selectedFeatures.length > 0) {
    return (
      <div className="feature-details">
        <h1>{selectedFeatures[0].name}</h1>
        <p>{selectedFeatures[0].description}</p>
      </div>
    );
  } else {
    return (
      <div className="feature-details">
        <h1>Select a feature to show its details...</h1>
      </div>
    );

  }
}

class FeaturesNavigator extends React.Component {
  render() {
    return (
      <div className="feature-navigator">
        <FeatureSearchBox onSearch={(searchString) => this.props.onSearch(searchString)}/>
        <FeaturesList features={this.props.features} onClickFeatureList={(i) => this.props.onClickNav(i)} />
      </div>
    );
  }
}

class FeatureSearchBox extends React.Component {

  constructor(props) {
    super(props);
    this.state = {value: ''};

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
    this.props.onSearch(event.target.value);
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <input className="search-box" type="text" value={this.state.value} onChange={this.handleChange} />
      </form>
    );
  }
}

class FeaturesList extends React.Component {

  render() {
    var features = this.props.features;
    return (
      <div className="features-list">
        {features.map((feature, index) => {
          return (
            <FeatureListItem key={index} name={feature.name} description={feature.description} selected={feature.selected} onClickFeatureListItem={() => this.props.onClickFeatureList(index)} visible={feature.visible}/>
          );
        })}
      </div>
    );
  }
}

function FeatureListItem(props) {
  var selectedStyle = {
    background: '#0099ff'
  };
  var regularStyle = {
    background: '#ffffff'
  };
  var dstyle = props.selected ? selectedStyle : regularStyle;

  if (!props.visible) {
    return null;
  }

  return (
    <div>
      <button className="feature-list-item" onClick={() => props.onClickFeatureListItem()} style={dstyle}>
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
