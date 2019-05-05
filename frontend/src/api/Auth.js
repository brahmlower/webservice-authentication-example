
const apiLoginRoute = '/api/auth'
const apiSignupRoute = '/api/signup'

function apiAuth (authRequest, onSuccess, onFailure) {
  fetch(apiLoginRoute, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(authRequest)
  })
  .then(response => response.json())
  .catch(error => console.log('Error: ', error))
  .then(appResponse => {
    // This is an application response. If it's null, there was an http error
    // somewhere along the way that wasn't translated into an app error (this
    // situation should be handled in all cases, and reaching 'undefined' here
    // is a programming error.
    if (typeof appResponse === 'undefined') { return; }
    if (appResponse.success === true) {
      // Authentication successful!
      onSuccess(appResponse);
    } else {
      // Authentication error
      onFailure(appResponse);
    }
  })
}

function apiSignup(signupRequest, onSuccess, onFailure) {
  fetch(apiSignupRoute, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(signupRequest)
  })
  .then(response => response.json())
  .catch(error => console.log('Error: ', error))
  .then(appResponse => {
    // This is an application response. If it's null, there was an http error
    // somewhere along the way that wasn't translated into an app error (this
    // situation should be handled in all cases, and reaching 'undefined' here
    // is a programming error.
    if (typeof appResponse === 'undefined') { return; }
    if (appResponse.success === true) {
      // Signup was successful!
      onSuccess(appResponse);
    } else {
      // Signup error
      onFailure(appResponse);
    }
  })
}

function apiLogout() {
  localStorage.removeItem('token')
  // this.forceUpdate();
}

export { apiAuth, apiSignup, apiLogout }
