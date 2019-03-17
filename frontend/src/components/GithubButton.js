import React, { Component } from 'react'
import { Button } from 'react-bootstrap';
import { apiAuth } from '../api/Auth';

function apiFailure (response) {
  console.log("Buildings API auth failure:", response)
}

function buildAuthRequest (token) {
  return {
    method: 'github',
    github: { token: token }
  }
}

class GithubButton extends Component {
  constructor(props) {
    super(props);
    this.oauthResponseSuccess = this.oauthResponseSuccess.bind(this);
    this.oauthResponseFailure = this.oauthResponseFailure.bind(this);
    this.successCallbackWrapper = this.successCallbackWrapper.bind(this);
  }

  successCallbackWrapper (response) {
    // Do some internal state processing if desired
    // Now call the auth success callback
    this.props.authSuccessCallback(response)
  }

  oauthResponseSuccess (response) {
    console.log("Oauth success:", response)
    // Build the buildings api request object
    let token = response.token // TODO: This is where the github oauth processing happens (see google for example)
    let bapiRequest = buildAuthRequest(token)
    // Make the buildings api call
    apiAuth(bapiRequest, this.successCallbackWrapper, apiFailure)
  }

  oauthResponseFailure (response) {
    console.log("Oauth failure:", response)
  }

  render () {
    return (
      <Button variant="outline-primary" disabled={this.props.disabled} block>
        <i className="fab fa-github" /> {this.props.label}
      </Button>
    )
  }
}

export { GithubButton }
