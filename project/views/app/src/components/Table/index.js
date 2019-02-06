import React, { Component } from "react";
import PropTypes from "prop-types";
import key from "weak-key";

class Table extends Component {
  constructor(props) {
    super(props);

    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(el) {
    this.props.editOnClick(el);
  }

  render() {
    const editClick = this.handleClick;

    return !this.props.data || !this.props.data.length ? (
      <p>Empty list.</p>
    ) : (
      <div>
        <table className="table table-striped">
          <thead>
            <tr>
              {this.props.columns.map(function(cl) {
                if (cl !== "id") return <th key={cl}>{cl}</th>;
                else return <th key={cl} />;
              })}
            </tr>
          </thead>
          <tbody>
            {this.props.data.map(el => (
              <tr key={el.id}>
                {this.props.columns.map(function(cl) {
                  if (cl !== "id") return <td key={key(el) + cl}>{el[cl]}</td>;
                  else
                    return (
                      <td key={key(el) + cl}>
                        {" "}
                        <button className="btn btn-link" onClick={() => editClick(el)}>
                          edit
                        </button>
                      </td>
                    );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
}

Table.propTypes = {
  data: PropTypes.array.isRequired,
  columns: PropTypes.array.isRequired,
  editOnClick: PropTypes.func.isRequired
};

export default Table;
