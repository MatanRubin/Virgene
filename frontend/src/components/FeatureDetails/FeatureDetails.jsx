import React from 'react';
import OptionSelect from '../OptionSelect/OptionSelect';
import OptionMultipleSelection from '../OptionMultipleSelection/OptionMultipleSelection';
import styles from './styles-feature-details.scss';

const FeatureDetails = (props) => {
  // TODO FeatureDetails should not calc which feature is selected, it should
  // be passed to it
  const selectedFeatures = props.features.filter(feature => feature.selected);
  const feature = selectedFeatures[0];
  if (selectedFeatures.length > 0) {
    return (
      <div className={styles.FeatureDetails}>
        <h1>{feature.name}</h1>
        <p>Type: {feature.feature_type}</p>
        <p>{feature.description}</p>
        {feature.options.map((option) => {
          switch (option.option_type) {
            case 'Choice': return (<OptionSelect option={option} />);
            case 'MultipleSelection': return (<OptionMultipleSelection option={option} />);
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
};

export default FeatureDetails;
