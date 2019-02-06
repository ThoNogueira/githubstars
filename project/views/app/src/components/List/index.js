import React, { Component } from "react";
import Search from '@material-ui/icons/Search';

import APIClient from "../../apiClient";
import Modal from "../Modal";
import Table from "../Table";
import Header from "../Header";

import "./style.css";

class List extends Component {
  constructor(props) {
    super(props);

    this.state = {
      showModal: false,
      repositories: null,
      repo: null,
      tags: [],
      searchTags: [],
      error: null
    };
    
    this.handleShow = this.handleShow.bind(this);
    this.handleHide = this.handleHide.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
    this.onChange = this.onChange.bind(this);
    this.apiClient = new APIClient();
  }

  handleShow(repo) {
    this.apiClient
      .getRepositoryTags(repo.id)
      .then(data =>
        this.setState({
          ...this.state,
          showModal: true,
          tags: data.map(tag => tag.name),
          repo: repo
        })
      )
      .catch(error => {
        if (
          error &&
          error.response &&
          error.response.data &&
          error.response.data.message
        )
          this.setState({ ...this.state, error: error.response.data.message });
        else this.setState({ ...this.state, error: JSON.stringify(error) });
      });
  }

  handleHide() {
    this.setState({ ...this.state, showModal: false, tags: [] });
  }

  componentDidMount() {
    this.apiClient
      .loadAllRepositories(this.props.match.params.gitLogin)
      .then(() => this.getRepositories())
      .catch(error => {
        if (
          error &&
          error.response &&
          error.response.data &&
          error.response.data.message
        )
          this.setState({ ...this.state, error: error.response.data.message });
        else this.setState({ ...this.state, error: JSON.stringify(error) });
      });
  }

  getRepositories = () => {
    this.apiClient
      .getRepositories(this.props.match.params.gitLogin, this.state.searchTags)
      .then(data =>
        this.setState({
          ...this.state,
          repositories: data
        })
      )
      .catch(error => {
        if (
          error &&
          error.response &&
          error.response.data &&
          error.response.data.message
        )
          this.setState({ ...this.state, error: error.response.data.message });
        else this.setState({ ...this.state, error: JSON.stringify(error) });
      });
  };

  onChange = e => {
    this.setState({
      ...this.state,
      tags: e.target.value.split(",").map(tag => tag.trim())
    });
  };

  searchOnChange = e => {
    this.setState({
      ...this.state,
      searchTags: e.target.value.split(",").map(tag => tag.trim())
    });
  };

  onSubmit = e => {
    e.preventDefault();
    this.apiClient
      .updateRepositoryTags(this.state.repo.id, this.state.tags)
      .then(() => {
        this.handleHide();
        this.getRepositories();
      })
      .catch(error => {
        if (
          error &&
          error.response &&
          error.response.data &&
          error.response.data.message
        )
          this.setState({ ...this.state, error: error.response.data.message });
        else this.setState({ ...this.state, error: JSON.stringify(error) });
      });
  };

  serachOnSubmit = e => {
    e.preventDefault();
    this.setState({
      ...this.state,
      repositories: null
    });
    this.getRepositories();
  };

  render() {
    const { tags, repo, showModal } = this.state;

    const modal = showModal ? (
      <Modal>
        <div className="modal" tabIndex="-1" role="dialog">
          <div className="modal-dialog modal-dialog-centered" role="document">
            <div className="modal-content">
              <form onSubmit={this.onSubmit}>
                <div className="modal-body">
                  <div className="form-group">
                    <label htmlFor="tags" className="col-form-label">
                      Edit tags for {repo.Repository}
                    </label>
                    <input
                      type="text"
                      className="form-control"
                      id="tags"
                      onChange={this.onChange.bind(this)}
                      defaultValue={tags || ""}
                    />
                  </div>
                </div>
                <div className="modal-footer">
                  <button
                    type="button"
                    className="btn btn-primary"
                    onClick={this.onSubmit.bind(this)}
                  >
                    Save
                  </button>
                  <button
                    type="button"
                    className="btn btn-secondary"
                    data-dismiss="modal"
                    onClick={this.handleHide}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </Modal>
    ) : null;

    return (
      (this.state && (this.state.repositories || this.state.error) && (
        <div>
          <Header showHome={true} />
          {this.state.error && (
            <div class="alert alert-danger" role="alert">
              Something is wrong... <br />
              {this.state.error}
            </div>
          )}
          <div className="p-3">
            <form className="form-inline" onSubmit={this.serachOnSubmit}>
              <div className="input-group">
                <div className="input-group-prepend">
                  <span className="input-group-text">
                    {" "}
                    <Search/>
                  </span>
                </div>
                <input
                  type="search"
                  defaultValue={this.state.searchTags}
                  onChange={this.searchOnChange.bind(this)}
                  className="form-control"
                  placeholder="Search by tag"
                />
              </div>
            </form>
          </div>
          <Table
            data={this.state.repositories}
            columns={["Repository", "Description", "Languages", "Tags", "id"]}
            editOnClick={this.handleShow}
          />
          {modal}
        </div>
      )) || (
        <React.Fragment>
          <Header />
          <div className="container-fluid h-75">
            <div className="row h-100 justify-content-center align-items-center flex-column">
              <div className="progress">
                <div
                  className="progress-bar progress-bar-striped progress-bar-animated"
                  role="progressbar"
                />
              </div>
              Getting the repositories list from Github...
            </div>
          </div>
        </React.Fragment>
      )
    );
  }
}

export default List;
