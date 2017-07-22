import React from 'react';

const OptionMultipleSelection = (props) => (
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

export default OptionMultipleSelection;
