import React, { Component } from 'react';
import { Switch, Route, BrowserRouter } from 'react-router-dom'
import { PageLanding } from './pages/Landing.js'
import { PageLogin } from './pages/Login.js'
import { PageSignup } from './pages/Signup.js'
import { PageHome } from './pages/Home.js'
import './App.css';

class App extends Component {
  render () {
    return (
      <BrowserRouter>
        <div className='App'>
            <Switch>
              <Route exact path='/' component={PageLanding} />
              <Route exact path='/login' component={PageLogin} />
              <Route exact path='/signup' component={PageSignup} />
              <Route exact path='/home' component={PageHome} />
            </Switch>
        </div>
      </BrowserRouter>
    )
  }
}

export default App;
