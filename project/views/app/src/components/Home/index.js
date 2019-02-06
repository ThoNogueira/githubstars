import React from "react";
import PlayArrowIcon from '@material-ui/icons/PlayArrow';

import Header from "../Header";

class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      login: null
    };

    this.onSubmit = this.onSubmit.bind(this);
    this.onChange = this.onChange.bind(this);
  }

  onChange = e => {
    this.setState({ ...this.state, login: e.target.value });
  };

  onSubmit = e => {
    e.preventDefault();
    if (this.state.login) this.props.history.push(`/list/${this.state.login}`);
  };

  render() {
    return (
      <div className="container-fluid h-75">
        <div className="row">
          <Header />
        </div>
        <div className="row h-100 justify-content-center align-items-center">
          <form onSubmit={this.onSubmit}>
            <div className="row">
              https://github.com/
              <input onChange={this.onChange} type="text" />
            </div>
            <div className="row justify-content-center p-3">
              <button
                onClick={this.onSubmit.bind(this)}
                className="btn btn-primary mb-5 d-flex justify-content-center align-content-between"
              >
                get repositories <PlayArrowIcon/>
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }
}

export default Home;
