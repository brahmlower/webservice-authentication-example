
const apiListRoute = "/api/buildings";

function handleAppResponse(appResponse, onSuccess, onFailure) {
  // This is an application response. If it's null, there was an http error
  // somewhere along the way that wasn't translated into an app error (this
  // situation should be handled in all cases, and reaching 'undefined' here
  // is a programming error.
  if (typeof appResponse === 'undefined') { return; }
  if (appResponse.success === true) {
    onSuccess(appResponse);
  } else {
    onFailure(appResponse);
  }
}

function apiListAll(onSuccess, onFailure) {
  fetch(apiListRoute, {
    method: 'GET',
    headers: {
      "Authorization": "Bearer " + localStorage.getItem('token')
    }
  })
  .then(response => response.json())
  .catch(error => console.log('Error: ', error))
  .then(appResponse => {
    handleAppResponse(appResponse, onSuccess, onFailure);
  })
}

export { apiListAll }
