import React, { Component } from 'react'
import { Button, Container, Row, Card } from 'react-bootstrap';
import { Redirect } from 'react-router-dom';
import { GoogleButton } from '../components/GoogleButton.js';
import { TwitterButton } from '../components/TwitterButton.js';
import { FacebookButton } from '../components/FacebookButton.js';
import { GithubButton } from '../components/GithubButton.js';
import { BuildingsLoginForm } from '../components/StandardLoginForm.js';
import { LoginPanelDisplay } from '../models/Auth.js';
import { isAuthed } from '../Common.js';

class MethodSelection extends Component {
  render () {
    let buildingsFn = () => this.props.nav(LoginPanelDisplay.BUILDINGS)
    let authCallback = this.props.authSuccessCallback
    return (
      <div>
        <GoogleButton label="With Google" disabled={false} authSuccessCallback={authCallback} />
        <TwitterButton label="With Twitter" disabled={true} authSuccessCallback={authCallback} />
        <FacebookButton label="With Facebook" disabled={true} authSuccessCallback={authCallback} />
        <GithubButton label="With Github" disabled={true} authSuccessCallback={authCallback} />
        <hr />
        <Button variant="outline-secondary" onClick={buildingsFn} block>
          <i class="far fa-building" /> With Buildings API
        </Button>
      </div>
    )
  }
}

class LoginPanel extends Component {
  constructor(props) {
    super(props);
    this.state = {
      panel: LoginPanelDisplay.SELECTION
    };
    this.setView = this.setView.bind(this);
    this.onAuthSuccess = this.onAuthSuccess.bind(this);
  }

  onAuthSuccess (response) {
    console.log("Page level auth callback got successful response!")
    localStorage.setItem('token', response.token);
    this.forceUpdate();
  }

  setView (view) {
    this.setState({ panel: view })
  }

  render() {
    if (isAuthed() === true) {
      return <Redirect to='/home' />
    }
    if (this.state.panel === LoginPanelDisplay.BUILDINGS) {
      return <BuildingsLoginForm authSuccessCallback={this.onAuthSuccess} nav={this.setView} />;
    } else {
      return <MethodSelection authSuccessCallback={this.onAuthSuccess} nav={this.setView} />;
    }
  }
}

class PageLogin extends Component {
  render () {
    return (<Container>
        <br />
        <br />
        <br />
        <Row>
          <div className="col-sm-4" style={{margin: 'auto'}}>
          <Card>
            <Card.Body>
              <Card.Title>Login</Card.Title>
              <LoginPanel />
            </Card.Body>
          </Card>
          </div>
        </Row>
      </Container>
    )
  }
}

export { PageLogin }
