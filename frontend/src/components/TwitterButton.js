import React, { Component } from 'react'
import { Button } from 'react-bootstrap';

class TwitterButton extends Component {
  render () {
    return (
      <Button variant="outline-primary" disabled={this.props.disabled} block>
        <i className="fab fa-twitter" /> {this.props.label}
      </Button>
    )
  }
}

export { TwitterButton }
