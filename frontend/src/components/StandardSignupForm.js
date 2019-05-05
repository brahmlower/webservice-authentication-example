import React, { Component } from 'react'
import { Form, Button, Alert } from 'react-bootstrap';
import { apiSignup } from '../api/Auth.js';
import { AuthPanelDisplay } from '../models/Auth.js';

function buildSignupRequest (name, username, password) {
  return {
    method: 'standard',
    standard: {
      name: name,
      username: username,
      password: password
    }
  }
}

class BuildingsSignupForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      name: '',
      username: '',
      password: '',
      passwordDup: '',
      nameError: null,
      usernameError: null,
      passwordError: null,
      passwordDupError: null,
      errors: []
    };
    this.formSubmit = this.formSubmit.bind(this);
    this.updateName = this.updateName.bind(this);
    this.updateUsername = this.updateUsername.bind(this);
    this.updatePassword = this.updatePassword.bind(this);
    this.updatePasswordDup = this.updatePasswordDup.bind(this);
    this.apiFailure = this.apiFailure.bind(this);
    this.successCallbackWrapper = this.successCallbackWrapper.bind(this);
  }

  successCallbackWrapper (response) {
    // Do some internal state processing if desired
    // Now call the success callback
    this.props.authSuccessCallback(response);
  }

  apiFailure (response) {
    let errorList = this.state.errors
    errorList.push(response)
    this.setState({ errors: errorList })
  }

  formSubmit () {
    console.log("Form submit initiated")
    // Build the buildings api request object
    let bapiRequest = buildSignupRequest(this.state.name, this.state.username, this.state.password)
    // Make the buildings api call
    apiSignup(bapiRequest, this.successCallbackWrapper, this.apiFailure);
  }

  updateName (event) {
    this.setState({ name: event.target.value })
  }

  updateUsername (event) {
    this.setState({ username: event.target.value })
  }

  updatePassword (event) {
    this.setState({ password: event.target.value })
  }

  updatePasswordDup (event) {
    this.setState({ passwordDup: event.target.value })
  }

  render () {
    let backFn = () => this.props.nav(AuthPanelDisplay.SELECTION)
    return (
      <Form>
        <Form.Group controlId="formBasicName">
          <Form.Control type="text" placeholder="Name" onChange={this.updateName} tabIndex={1} autoFocus />
        </Form.Group>
        <Form.Group controlId="formBasicEmail">
          <Form.Control type="text" placeholder="Username" onChange={this.updateUsername} tabIndex={2} />
        </Form.Group>
        <Form.Group controlId="formBasicPassword">
          <Form.Control type="password" placeholder="Password" onChange={this.updatePassword} tabIndex={3} />
        </Form.Group>
        <Form.Group controlId="formBasicPasswordDup">
          <Form.Control type="password" placeholder="Repeat Password" onChange={this.updatePasswordDup} tabIndex={4} />
        </Form.Group>
        <Form.Group style={{overflow: "hidden"}}>
          <Button variant="outline-secondary" onClick={backFn} className="float-left" tabIndex={5}> Cancel </Button>
          <Button variant="primary" className="float-right" tabIndex={6} onClick={this.formSubmit}> Submit </Button>
        </Form.Group>
        <div className="signupErrors">
          {this.state.errors.map( (error, idx) => {
            console.log(error.response)
            return (
              <Alert key={idx} dismissible variant="danger"> { error.response.message } </Alert>
            )
          })}
        </div>
      </Form>
    )
  }
}

export { BuildingsSignupForm }
