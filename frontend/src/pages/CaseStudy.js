import React, { Component } from 'react'
import { BuildingsNavbar } from '../components/Navbar.js'

class PageCaseStudy extends Component {
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
        <p> Case Study </p>
      </div>
    )
  }
}

export { PageCaseStudy }
