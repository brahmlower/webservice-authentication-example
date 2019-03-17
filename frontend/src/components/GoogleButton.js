import React, { Component } from 'react'
import { Button } from 'react-bootstrap';
import { GoogleLogin } from 'react-google-login';
import { apiAuth } from '../api/Auth.js';

const googleClientId = '707989048789-cnbimfp18p0547hptm4af4p6sphe5e10.apps.googleusercontent.com';

function apiFailure (response) {
  console.log("FAILURE!", response)
}

function buildAuthRequest (token) {
  return {
    method: 'google',
    google: { token: token }
  };
}

class GoogleButton extends Component {
  constructor(props) {
    super(props);
    this.oauthResponseSuccess = this.oauthResponseSuccess.bind(this);
    this.oauthResponseFailure = this.oauthResponseFailure.bind(this);
    this.successCallbackWrapper = this.successCallbackWrapper.bind(this);
  }

  successCallbackWrapper (response) {
    // Do some internal state processing if desired
    // Now call the success callback
    this.props.authSuccessCallback(response);
  }

  oauthResponseSuccess (response) {
    console.log("Oauth success:", response)
    // Build the buildings api request object
    let token = response.getAuthResponse().id_token;
    let bapiRequest = buildAuthRequest(token);
    // The ID token you need to pass to your backend:
    apiAuth(bapiRequest, this.successCallbackWrapper, apiFailure);
  }

  oauthResponseFailure (response) {
    console.log(response)
  }

  render () {
    return (
      <GoogleLogin
        clientId={googleClientId}
        buttonText="Login"
        render={renderProps => (
          <Button variant="outline-primary" onClick={renderProps.onClick} block>
            <i className="fab fa-google" /> {this.props.label}
          </Button>
        )}
        onSuccess={this.oauthResponseSuccess}
        onFailure={this.oauthResponseFailure}
      />
    )
  }
}

export { GoogleButton }
