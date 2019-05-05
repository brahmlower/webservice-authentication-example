import React, { Component } from 'react'
import { Redirect } from 'react-router-dom';
import { isAuthed } from '../Common.js';
import { BuildingsNavbar } from '../components/Navbar.js'

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
    // Redirect user to index if they're not logged in
    if (isAuthed() === false) {
      return <Redirect to='/' />
    }
    // Build the page as usual
    return (
      <div>
        <BuildingsNavbar />
        <p>This is the HOME PAGE</p>
      </div>
    )
  }
}

export { PageHome }
