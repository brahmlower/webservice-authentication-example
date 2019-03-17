import React, { Component } from 'react';
import { Switch, Route, BrowserRouter } from 'react-router-dom'
import { PageLanding } from './pages/Landing.js'
import { PageLogin } from './pages/Login.js'
import { PageSignup } from './pages/Signup.js'
// import { PageHome } from './pages/Home.js'
// import { Page }
// import { Container } from
// import logo from './logo.svg';
import './App.css';

class App extends Component {
  render () {
    return (
      <BrowserRouter>
        <div className='App'>
          {/* <Container> */}
            {/* <h1> Authenticated Building Service </h1> */}
            <Switch>
              <Route exact path='/' component={PageLanding} />
              <Route exact path='/login' component={PageLogin} />
              <Route exact path='/signup' component={PageSignup} />
            </Switch>
          {/* </Container> */}
        </div>
      </BrowserRouter>
    )
  }
}


// class App extends Component {
//   render() {
//     return (
//       <div className="App">
//         <header className="App-header">
//           <img src={logo} className="App-logo" alt="logo" />
//           <p>
//             Edit <code>src/App.js</code> and save to reload.
//           </p>
//           <a
//             className="App-link"
//             href="https://reactjs.org"
//             target="_blank"
//             rel="noopener noreferrer"
//           >
//             Learn React
//           </a>
//         </header>
//       </div>
//     );
//   }
// }

export default App;
