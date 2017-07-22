import React from 'react';
import styles from './styles-feature-search-box.scss';

export default class FeatureSearchBox extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      value: '',
    };

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
    this.props.onSearch(event.target.value);
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <input
          className={styles.FeatureSearchBox}
          type="text"
          value={this.state.value}
          onChange={this.handleChange}
        />
      </form>
    );
  }
}
