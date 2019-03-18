import React, { Component } from 'react'
import { Button } from 'react-bootstrap';
import { Redirect } from 'react-router-dom';
import { isAuthed, linkButtonStyle } from '../Common.js';

class PageHome extends Component {
  constructor(props) {
    super(props);
    this.logout = this.logout.bind(this);
  }

  logout() {
    localStorage.removeItem('token')
    this.forceUpdate();
  }

  render () {
    if (isAuthed() === false) {
      return <Redirect to='/' />
    } else {
      return (
        <div>
          <p>This is the HOME PAGE</p>
          <Button variant="link" style={linkButtonStyle} onClick={this.logout}> Logout </Button>
        </div>
      )
    }
  }
}

export { PageHome }
