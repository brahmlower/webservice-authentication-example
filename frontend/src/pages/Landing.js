import React, { Component } from 'react'

class PageLanding extends Component {
  render () {
    return (
      <div>
        <p> This is the landing page! </p>
        <a href="/login"> Login </a> or <a href="/signup"> Sign Up </a>
      </div>
    )
  }
}

export { PageLanding }
