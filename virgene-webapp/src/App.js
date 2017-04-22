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
        <div className="features-config">
          {/* this.renderFeature(0)}
          {this.renderFeature(1)}
          {this.renderFeature(2)}
          {this.renderFeature(3) */}
          <FeaturesNavigator/>
          <FeatureDetails/>
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
  return (
    <h1>asdasd</h1>
  );
}

function FeatureListItem(props) {
  var selectedStyle = {
    background: '#0099ff'
  };
  var regularStyle = {
    background: '#ffffff'
  };
  var dstyle = props.selected ? selectedStyle : regularStyle;

  return (
    <div>
      <button className="feature-list-item" onClick={() => props.onClick()} style={dstyle}>
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

class FeatureSearchBox extends React.Component {

  constructor(props) {
    super(props);
    this.state = {value: ''};

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
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
    return (
      <div>
        <FeatureListItem name="feature1" description="feature1 description" selected={true}/>
        <FeatureListItem name="feature2" description="feature2 description" selected={false}/>
        <FeatureListItem name="feature3" description="feature3 description" selected={false}/>
        <FeatureListItem name="feature4" description="feature4 description" selected={false}/>
        <FeatureListItem name="feature5" description="feature5 description" selected={false}/>
        <FeatureListItem name="feature6" description="feature6 description" selected={false}/>
        <FeatureListItem name="feature7" description="feature7 description" selected={false}/>
        <FeatureListItem name="feature8" description="feature8 description" selected={false}/>
        <FeatureListItem name="feature9" description="feature9 description" selected={false}/>
      </div>
    );
  }
}

class FeatureDetails extends React.Component {
  render() {
    return (
      <div className="feature-details">
        <h1>Feature Name</h1>
        <p>Feature description...</p>
      </div>
    );
  }
}

class FeaturesNavigator extends React.Component {
  render() {
    return (
      <div className="feature-navigator">
        <FeatureSearchBox/>
        <FeaturesList/>
      </div>
    );
  }
}

export default App;
