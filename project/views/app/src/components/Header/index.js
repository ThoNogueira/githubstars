import React from "react";
import "./style.css";

class Header extends React.Component {
  render() {
    return (
      <div className="header">
        <div className="item">
          <h1>githubstars</h1>
        </div>
        {this.props.showHome && (
          <div className="item">
            <a href="/">home</a>
          </div>
        )}
      </div>
    );
  }
}

export default Header;
