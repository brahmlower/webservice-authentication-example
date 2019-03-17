import React, { Component } from 'react'
import { SiteMenu } from '../components/Menu'

class PageAbout extends Component {
  render () {
    return (
      <div>
        <SiteMenu location={ this.props.location }/>
        <p> This is a service hosting information about large buildings. </p>
      </div>
    )
  }
}

export { PageAbout }
