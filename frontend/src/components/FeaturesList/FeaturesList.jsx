import React from 'react';
import FeaturesListItem from '../FeaturesListItem/FeaturesListItem';
import styles from './styles-features-list.scss';

export default class FeaturesList extends React.Component {

  render() {
    const features = this.props.features;
    return (
      features.length > 0 ?
      <div className={styles.FeaturesList}>
        {
          features.map(feature => (
            <FeaturesListItem
              key={feature.name}
              name={feature.name}
              description={feature.description}
              selected={feature.selected}
              onClickFeatureListItem={() => this.props.onClickFeatureList(feature.name)}
              visible={feature.visible}
            />
          ))
        }
      </div> :
      <div>
        <div>Couldn't find what you were looking for?</div>
        <div>Contribute a feature!</div>
      </div>
    );
  }
}
