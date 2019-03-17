
const apiAuthRoute = '/api/auth'

function apiAuth (authRequest, onSuccess, onFailure) {
  fetch(apiAuthRoute, {
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

export { apiAuth }
