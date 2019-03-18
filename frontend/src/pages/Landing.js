import React, { Component } from 'react'
// import { Link } from 'react-router-dom'
import { Jumbotron, Container, Button, Nav, Navbar } from 'react-bootstrap';
// import { linkButtonStyle } from '../Common.js';
import './Landing.css';

// https://www.kisspng.com/png-high-rise-building-skyscraper-vector-skyscrapers-95811/
const buildingImageUrl = "https://png2.kisspng.com/sh/7b46047055b586d6d02374c1aaf11601/L0KzQYm3UcI5N6luj5H0aYP2gLBuTfhqb5kyitt8ZT3lhbrzhPlvb154gAt8Y4LkgLb5TgZma6V0ip98a4n2c8PokPVze146eahuMUS5RbOCUBU6PF83TqsCM0K0SYK8UccyPmQ7SqMCNUi7PsH1h5==/kisspng-high-rise-building-skyscraper-vector-skyscrapers-5a6e1465b93e94.2697321915171636217588.png"
// const checkerImageUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Checkermotoslogo.svg/240px-Checkermotoslogo.svg.png"
const buildingJsonUrl = "/buildings_json.png"
// const loginLink = (
//   <Link to="/login">
//     <Button variant="link" style={linkButtonStyle}>
//       Login
//     </Button>
//   </Link>
// )

// const signupLink = (
//   <Link to="/signup">
//     <Button variant="link" style={linkButtonStyle}>
//       Sign Up
//     </Button>
//   </Link>
// )

class InteractiveGraphic extends Component {
  render () {
    return (
      <div className="jumbotronImg">
        <img src={buildingJsonUrl} height="400" withd="400" id="codeImg" alt="black and white checker pattern" />
        <img src={buildingImageUrl} height="400" width="400" id="buildingImg" alt="vector art of building" />
      </div>
    )
  }
}

class PageLanding extends Component {
  render () {
    return (
      <div>
        <Navbar bg="custom" variant="light">
          <Navbar.Brand href="/">BuildingsAPI</Navbar.Brand>
          <Navbar.Collapse>
            <Nav className="mr-auto">
              <Nav.Link href="/home">Home</Nav.Link>
              <Nav.Link href="/casestudy">Case Study</Nav.Link>
              <Nav.Link href="/about">About</Nav.Link>
            </Nav>
            <Button variant="outline-secondary" style={{marginRight: 8}}>Login</Button>
            <Button variant="outline-primary">Sign Up</Button>
          </Navbar.Collapse>
        </Navbar>
        <Jumbotron fluid style={{margin: 0}}>
          <Container>
            <div className="row align-items-center">
              <div className="col-6 mx-auto col-md-6 order-md-2 text-md-left">
                <h1>BuildingsAPI</h1>
                <p>
                  This project is to exemplify various authentication mechanisms
                  for webservices, including multiple Oauth sources, 2fa, API
                  token generation, and best practices for password storage.
                </p>
                <p>
                  This service operates as a functioning API, representing a
                  typical web service. You can log in with any available Oauth
                  provider or standalone credentials to explore the functionality
                  demonstrated in this project. Sign up to begin exploring, or
                  login with the <strong> Test </strong> account to test with
                  limited account access.
                </p>
              </div>
              <div className="col-6 col-md-6 order-md-2">
                <InteractiveGraphic />
              </div>
            </div>
          </Container>
        </Jumbotron>
        <div className="masthead-followup row m-0 border border-white">
          {/* Oauth providers information card */}
          <div className="col-12 col-md-4 p-3 p-md-5 bg-light border border-white text-md-left">
            <h3>Oauth Implementations</h3>
            <p>
              This shows examples of integrating Oauth providers into an existing
              standalone authentication mechanism. Current supported Oauth
              providers are: Google, Twitter, Facebook, Github
            </p>
          </div>
          {/* 2fa information card */}
          <div className="col-12 col-md-4 p-3 p-md-5 bg-light border border-white text-md-left">
            <h3>Password Best Practices</h3>
            <p>
              Password storage is a pain in the ass, and always an interesting
              point of observation during data breaches. Proper password storage
              can minimise damages and liability (?) during breaches.
            </p>
          </div>
          {/* Password storage information */}
          <div className="col-12 col-md-4 p-3 p-md-5 bg-light border border-white text-md-left">
            <h3>2fa Support</h3>
            <p>
              Two factor authentication is increasingly important! This project
              incorporates some best practices about 2fa support.
            </p>
          </div>
        </div>
        <div className="bd-footer text-muted">
          <div className="container-fluid p-3 p-md-5">
            <p>Currently v0.1.0. Code licensed TDB.</p>
          </div>
        </div>
      </div>
    )
  }
}

export { PageLanding }
