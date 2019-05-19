import React, { Component } from 'react'
import { Button } from 'react-bootstrap';
import './Dashboard.css';
import { apiListAll } from '../api/Buildings.js';


class SearchForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      results: []
    };
    this.searchSuccess = this.searchSuccess.bind(this);
    this.searchFailed = this.searchFailed.bind(this);
    this.submitSearch = this.submitSearch.bind(this);
  }

  searchSuccess (appResponse) {
    this.setState({
      results: appResponse.response
    });
  }

  searchFailed (appResponse) {
    console.log(appResponse);
    alert('Failed to search :(');
  }

  submitSearch () {
    apiListAll(this.searchSuccess, this.searchFailed);
  }

  render () {
    return (
      <div>
        <Button onClick={this.submitSearch}>Search</Button>
        <table className="table">
          <thead>
            <th scope='col'>Picture</th>
            <th scope='col'>Name</th>
            <th scope='col'>Height</th>
            <th scope='col'>Description</th>
            <th scope='col'>City</th>
            <th scope='col'>Country</th>
          </thead>
          <tbody>
            {this.state.results.map( (building, idx ) => {
              return (
                <tr key={ idx }>
                  <td>{ building.image_url }</td>
                  <td>{ building.name }</td>
                  <td>{ building.height }</td>
                  <td>{ building.description }</td>
                  <td>{ building.city }</td>
                  <td>{ building.country }</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    );
  }
}

class Search extends Component {
  render () {
    return (
      <div>
        <div className="dashboardSection">
          <h1>Search</h1>
        </div>

        <div className="dashboardSection">
          <SearchForm />
        </div>

      </div>
    );
  }
}

export { Search }
