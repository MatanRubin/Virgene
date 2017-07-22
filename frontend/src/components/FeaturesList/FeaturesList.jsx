import React from 'react';
import FeaturesListItem from '../FeaturesListItem/FeaturesListItem';
import styles from './styles-features-list.scss';

export default class FeaturesList extends React.Component {

  render() {
    const features = this.props.features;
    return (
      <div className={styles.FeaturesList}>
        {features.map((feature, index) => {
          return (
            <FeaturesListItem
              key={index}
              name={feature.name}
              description={feature.description}
              selected={feature.selected}
              onClickFeatureListItem={() => this.props.onClickFeatureList(index)}
              visible={feature.visible}
            />
          );
        })}
      </div>
    );
  }
}
