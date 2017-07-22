import React from 'react';
import styles from './styles-features-list-item.scss';

const FeaturesListItem = (props) => {
  const selectedStyle = {
    background: '#0099ff',
  };
  const regularStyle = {
    background: '#ffffff',
  };
  const dstyle = props.selected ? selectedStyle : regularStyle;

  if (!props.visible) {
    return null;
  }

  return (
    <div>
      <button className={styles.FeaturesListItem} onClick={() => props.onClickFeatureListItem()} style={dstyle}>
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
