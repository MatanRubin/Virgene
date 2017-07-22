import React from 'react';

const OptionSelect = (props) => (
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

export default OptionSelect;
