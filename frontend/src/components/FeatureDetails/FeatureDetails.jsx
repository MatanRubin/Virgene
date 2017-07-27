import React from 'react';
import OptionSelect from '../OptionSelect/OptionSelect';
import OptionMultipleSelection from '../OptionMultipleSelection/OptionMultipleSelection';
import styles from './styles-feature-details.scss';

const FeatureDetails = props => (
  props.selectedFeature ?
  <div className={styles.FeatureDetails}>
    <h1>{props.selectedFeature.name}</h1>
    <p>Type: {props.selectedFeature.feature_type}</p>
    <p>{props.selectedFeature.description}</p>
    {
      props.selectedFeature.options ?
        props.selectedFeature.options.map((option) => {
          switch (option.option_type) {
            case 'Choice':
              return (
                <OptionSelect
                  name={option.name}
                  description={option.description}
                  options={option.options}
                  multi={false}
                />);
            case 'MultipleSelection':
              return (
                <OptionSelect
                  name={option.name}
                  description={option.description}
                  options={option.options}
                  multi={true}
                />);
            default: return (<p>{option.name}</p>);
          }
        }) :
        null
    }
  </div> :
  <div className={styles.noSelection}>Select a feature to show its details...</div>
);

export default FeatureDetails;
