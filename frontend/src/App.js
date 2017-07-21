import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  constructor() {
    super();
    this.state = {
      features: [
        {
          "name": "CtrlP",
          "identifier": "ctrlp",
          "feature_type": "Plugin",
          "description": "Full path fuzzy file, buffer, mru, tag, ... finder for Vim.",
          "enabled": false,
          "selected": true,
          "visible": true,
          "category": "Navigation",
          "installed": true,
          "template": "ctrlp.j2",
          "vundle_installation": "ctrlpvim/ctrlp.vim",
          "options":
          [
            {
                "name": "CtrlP Command",
                "identifier": "ctrlp_cmd",
                "option_type": "Choice",
                "choices": ["CtrlPMixed", "CtrlPStam", "CtrlPDrek"],
                "pretty_name": "CtrlP Command",
                "description": "Which mode should CtrlP start in",
                "default_value": "CtrlPMixed"
            },
            {
                "name": "CtrlP Extensions",
                "identifier": "ctrlp_extensions",
                "option_type": "MultipleSelection",
                "pretty_name": "CtrlP Extensions",
                "description": "Select which CtrlP extensions to enable",
                "default_value": ["dir", "mixed"],
                "choices": ["tag", "buffertag", "quickfix", "dir", "rtscript", "undo", "line", "changes", "mixed", "bookmarkdir"]
            },
            {
                "name": "CtrlP working path mode",
                "identifier": "ctrlp_working_path_mode",
                "option_type": "MultipleSelection",
                "choices": ["c", "a", "r", "w", "0"],
                "pretty_name": "CtrlP working path mode",
                "description": "How should CtrlP choose its working directory when starting?",
                    "details": "c - the directory of the current file.\na - like \"c\", but only applies when the current working directory outside of CtrlP isn't a direct ancestor of the directory of the current file.\nr - the nearest ancestor that contains one of these directories or files: .git .hg .svn .bzr _darcs\nw - begin finding a root from the current working directory outside of CtrlP instead of from the directory of the current file (default). Only applies when \"r\" is also present.\n 0 or <empty> - disable this feature.",
                "default_value": "r"
            }
          ]
        },
        {
          name: "Tagbar",
          description: "Tag browser",
          selected: false,
          visible: true,
        },
        {
          name: "Disable arrow keys",
          description: "Disable arrow keys, helps you learn to use just hjkl",
          selected: false,
          visible: true,
        },
        {
          name: "Highlight search",
          description: "Highlight search results",
          selected: false,
          visible: true,
        },
      ]
    };
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
  // TODO FeatureDetails should not calc which feature is selected, it should
  // be passed to it
  var selectedFeatures = props.features.filter(function(feature) {
    return feature.selected;
  });
  var feature = selectedFeatures[0];
  if (selectedFeatures.length > 0) {
    return (
      <div className="feature-details">
        <h1>{feature.name}</h1>
        <p>Type: {feature.feature_type}</p>
        <p>{feature.description}</p>
        {feature.options.map((option, index) => {
          switch (option.option_type) {
            case 'Choice': return (<ChoiceOption option={option}/>);
            case 'MultipleSelection': return (<MultipleSelectionOption option={option}/>);
            default: return (<p>{option.name}</p>);
          }
        })}
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

function MultipleSelectionOption(props) {
  return (
    <div>
      <h2>{props.option.name}</h2>
      <p>{props.option.description}</p>
        <select multiple>
          {props.option.choices.map((choice, index) => {
            return (
              <option key={index} value={choice}>{choice}</option>
            );
          })}
        </select>
    </div>
  );
}

function ChoiceOption(props) {
  return (
    <div>
      <h2>{props.option.name}</h2>
      <p>{props.option.description}</p>
        <select>
          {props.option.choices.map((choice, index) => {
            return (
              <option key={index} value={choice}>{choice}</option>
            );
          })}
        </select>
    </div>
  );
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
