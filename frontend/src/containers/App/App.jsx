import React from 'react';
import FeatureDetails from '../../components/FeatureDetails/FeatureDetails';
import FeaturesNavigator from '../../components/FeaturesNavigator/FeaturesNavigator';
import styles from './App.scss';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filteredFeatures: props.features,
      selectedFeature: null,
    };
  }

  handleClick(featureName) {
    const features = this.props.features.slice();
    features.map(feature => feature.selected = false);
    const selectedFeature = features.find(feature => feature.name === featureName);
    selectedFeature.selected = true;
    this.setState({ features, selectedFeature });
  }

  handleSearch(searchString) {
    const filteredFeatures = this.props.features.filter(
      feature => feature.name.toLowerCase().includes(searchString.toLowerCase()));
    this.setState({ filteredFeatures });
  }

  render() {
    return (
      <div className={styles.App}>
        <div className={styles.appHeader}>
          <h2>Virgene</h2>
          <h3>Extensible, easy to use vimrc generator</h3>
        </div>
        <p className={styles.appIntro}>
          Enable and configure Vim features.
        </p>
        <div className={styles.featuresConfig}>
          <FeaturesNavigator
            features={this.state.filteredFeatures}
            onClickNav={featureName => this.handleClick(featureName)}
            onSearch={searchString => this.handleSearch(searchString)}
          />
          <FeatureDetails selectedFeature={this.state.selectedFeature} />
        </div>
      </div>
    );
  }
}
