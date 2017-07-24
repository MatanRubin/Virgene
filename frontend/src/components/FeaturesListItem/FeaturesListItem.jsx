import React from 'react';
import styles from './styles-features-list-item.scss';

const FeaturesListItem = (props) => {
  if (!props.visible) {
    return null;
  }

  return (
    <div className={styles.FeaturesListItem}>
      <span className={`${styles.selectedMarker} ${props.selected ? styles.selected : null}`}></span>
      <button className={styles.details} onClick={() => props.onClickFeatureListItem()}>
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

export default FeaturesListItem;
