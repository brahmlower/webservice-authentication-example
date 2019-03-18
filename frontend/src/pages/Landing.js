import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { Button } from 'react-bootstrap';
import { linkButtonStyle } from '../Common.js';

const loginLink = (
  <Link to="/login">
    <Button variant="link" style={linkButtonStyle}>
      Login
    </Button>
  </Link>
)

const signupLink = (
  <Link to="/signup">
    <Button variant="link" style={linkButtonStyle}>
      Sign Up
    </Button>
  </Link>
)

class PageLanding extends Component {
  render () {
    return (
      <div>
        <p>This is the landing page! {loginLink} or {signupLink}</p>
      </div>
    )
  }
}

export { PageLanding }
