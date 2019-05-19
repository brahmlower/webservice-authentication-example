import React, { Component } from 'react'
import { Redirect } from 'react-router-dom';
import { Tab, Row, Col, ListGroup, Container } from 'react-bootstrap';
import { isAuthed } from '../Common.js';
import { BuildingsNavbar } from '../components/Navbar.js';
import { Dashboard } from '../components/Dashboard.js';
import { Search } from '../components/Search.js';
import './Home.css';

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

        <div>
          <Container fluid style={{textAlign: 'left'}}>

            <Tab.Container id="list-group-tabs-example" defaultActiveKey="#dashboard">
              <Row className="pageContent">
                <Col sm={2} className="sideNavBar">
                  <ListGroup variant="flush">
                    <ListGroup.Item action href="#dashboard">Dashboard</ListGroup.Item>
                    <ListGroup.Item action href="#search">Search</ListGroup.Item>
                  </ListGroup>
                </Col>
                <Col sm={10} className="contentPane">
                  <Tab.Content>
                    <Tab.Pane eventKey="#dashboard"><Dashboard /></Tab.Pane>
                    <Tab.Pane eventKey="#search"><Search /></Tab.Pane>
                  </Tab.Content>
                </Col>
              </Row>
            </Tab.Container>

          </Container>
        </div>

      </div>
    )
  }
}

export { PageHome }
