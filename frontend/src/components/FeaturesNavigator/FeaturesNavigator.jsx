import React from 'react';
import FeatureSearchBox from '../FeatureSearchBox/FeatureSearchBox';
import FeaturesList from '../FeaturesList/FeaturesList';
import styles from './styles-features-navigator.scss';

const FeaturesNavigator = props => (
  <div className={styles.FeaturesNavigator}>
    <FeatureSearchBox onSearch={(searchString) => props.onSearch(searchString)} />
    <FeaturesList features={props.features} onClickFeatureList={i => props.onClickNav(i)} />
  </div>
);

export default FeaturesNavigator;
