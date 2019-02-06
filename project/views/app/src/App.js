import React, { Component } from "react";
import { Switch, Route, BrowserRouter as Router } from "react-router-dom";
import Home from "./components/Home";
import List from "./components/List";

class App extends Component {
  render() {
    return (
      <Router>
        <Switch>
          <Route path="/" component={Home} exact />
          <Route path="/list/:gitLogin" component={List} />
        </Switch>
      </Router>
    );
  }
}

export default App;
