import React from 'react';
import Select from 'react-select';
import 'react-select/dist/react-select.css';

export default class OptionSelect extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      value: null,
    };
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(value) {
    this.setState({ value });
  }

  render() {
    return (
      <div>
        <h2>{this.props.name}</h2>
        <p>{this.props.description}</p>
        <Select
          value={this.state.value}
          options={this.props.options.map((option) => {
            return { value: option, label: option };
          })}
          searchable={false}
          onChange={this.handleChange}
          clearable={false}
          multi={this.props.multi ? this.props.multi : false}
        />
      </div>
    );
  }
}
