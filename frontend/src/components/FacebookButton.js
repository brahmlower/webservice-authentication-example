import React, { Component } from 'react'
import { Button } from 'react-bootstrap';

class FacebookButton extends Component {
  render () {
    return (
      <Button variant="outline-primary" disabled={this.props.disabled} block>
        <i className="fab fa-facebook" /> {this.props.label}
      </Button>
    )
  }
}

export { FacebookButton }
