import React, { Component } from 'react'
import { BuildingsNavbar } from '../components/Navbar.js'

class PageAbout extends Component {
  constructor(props) {
    super(props);
    this.logout = this.logout.bind(this);
  }

  logout() {
    localStorage.removeItem('token')
    this.forceUpdate();
  }

  render () {
    return (
      <div>
        <BuildingsNavbar />
        <p> About The Project </p>
      </div>
    )
  }
}

export { PageAbout }
