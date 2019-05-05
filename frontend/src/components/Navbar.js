
import React, { Component } from 'react'
import { Link } from 'react-router-dom';
import { Button, Nav, Navbar } from 'react-bootstrap';
import { isAuthed } from '../Common.js';
import { apiLogout } from '../api/Auth.js'

class BuildingsNavbar extends Component {

  constructor(props) {
    super(props);
    this.logout = this.logout.bind(this);
  }

  logout() {
    apiLogout()
    this.forceUpdate();
  }

  render () {
    let authed = isAuthed()
    console.log("Auth status:", authed)
    const authedButtons = (
      <div>
        <Button variant="outline-primary" style={{marginRight: 8}}><Link to="/home">Home</Link></Button>
        <Button variant="outline-secondary" onClick={this.logout}> Logout </Button>
      </div>
    )
    const unauthedButtons = (
      <div>
        <Button variant="outline-secondary" style={{marginRight: 8}}><Link to="/login">Login</Link></Button>
        <Button variant="outline-primary"><Link to="/signup">Sign Up</Link></Button>
      </div>
    )
    let accountNavButtons = (authed) ? authedButtons : unauthedButtons
    return (
      <Navbar bg="custom" variant="light">
        <Navbar.Brand href="/">
          <i class="far fa-building" /> BuildingsAPI
        </Navbar.Brand>
        <Navbar.Collapse>
          <Nav className="mr-auto">
            <Nav.Link><Link to="/casestudy">Case Study</Link></Nav.Link>
            <Nav.Link><Link to="/about">About</Link></Nav.Link>
          </Nav>
          {accountNavButtons}
        </Navbar.Collapse>
      </Navbar>
    )
  }
}

export { BuildingsNavbar }
