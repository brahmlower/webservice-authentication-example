
import os
import sys
import unittest
import json

sys.path.append('../')

from src import BuildingsApi

""" Testing API responses

All API responses are required to have to keys in the root data structure,
regardless of what data is being returned:

 - success
 - response

These are pretty straightforward- success is a boolean indicating if the application
requests was able to fufill the request, and response is the requested data structure.

In the context of testing, it can safely be assumed that all responses will
adhere to this format, so there is no need to explicitely verify the presence of
these keys. For example, the following assertion is unnecessary:

```
self.assertTrue('success' in data.keys())
``

Instead, it is reasonable to write assertions that make the assumption that they
required key exists.

```
self.assertTrue(data.get('success'))
```

Likewise, in cases where an error is being asserted, there is no need to assert
particular keys in the 'response' structure. All errors returned in a controlled
manner are constructed in a similar way, and are garanteed (as much as can be in
python) to have the correct structure. Therefore the following is unnecessary

```
self.assertTrue('error' in data.get('response').keys())
self.assertTrue('message' in data.get('response').keys())
```

Instead, the following are reasonable assertions on an error response:

```
self.assertEqual(data.get('response').get('error'), 'MissingRequiredHeader')
self.assertTrue(len(data.get('response').get('message')) > 0 )
```

It is reasonable, and highly recommended, that assertions be written for other
response data structures.

"""

PUBLIC_USER_ID = 0
DEFAULT_USER_ID = 1
DEFAULT_USERNAME = 'bob'
DEFAULT_PASSWORD = 'burgers'

def build_server_config(db_hostname='localhost', db_database='buildings_db',
        db_username='service_user', db_password='service_user_password',
        db_port=5432, auth_jwt_secret='buttsbuttsbutts', auth_jwt_algo='HS256',
        backends_google_client_id='stubstubstub!'):
    """ Gross function for easily building customizable configs """
    return {
        'db': {
            'hostname': db_hostname,
            'database': db_database,
            'username': db_username,
            'password': db_password,
            'port': db_port
        },
        'auth': {
            'jwt': {
                'secret': auth_jwt_secret,
                'algo': auth_jwt_algo
            },
            'backends': {
                'google': {
                    'client_id': backends_google_client_id
                }
            }
        }
    }

class TestBuildingsAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.server_config = build_server_config()
        self.server = BuildingsApi(self.server_config)
        self.server.testing = True # Not sure what this does for us
        self.client = self.server.test_client()

    def tearDown(self):
        pass

    def _standard_login_request(self, username, password):
        auth_dict = {
            'method': 'standard',
            'standard': {
                'username': username,
                'password': password
            }
        }
        request_data = json.dumps(auth_dict)
        return self.client.post('/api/auth', data=request_data, content_type='application/json')

    def _standard_login(self, username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD):
        auth_response = self._standard_login_request(username, password)
        raw_token = json.loads(auth_response.data)['response']['token']
        bearer_token = 'Bearer {}'.format(raw_token)
        return bearer_token

    def test_index(self):
        response = self.client.get('/')
        data = json.loads(response.data)
        assert 'message' in data.keys()

    def test_standard_login_okay(self):
        result = self._standard_login_request(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertTrue(data.get('success'))
        self.assertTrue('token' in data['response'].keys())

    def test_standard_login_bad_credentials(self):
        valid_username = DEFAULT_USERNAME
        invalid_username = 'linda'
        invalid_password = 'wine'
        # Get response with good username, but bad password
        # bpr = Bad Password Response
        bpr = self._standard_login_request(DEFAULT_USERNAME, invalid_password)
        self.assertEqual(bpr.status_code, 400)
        bpr_data = json.loads(bpr.data)
        # bpr assertions
        self.assertFalse(bpr_data.get('success'))
        self.assertEqual(bpr_data.get('response').get('error'), 'StandardAuthFailure')
        # Get response with bad username and bad password
        # bur = Bad Username Response
        bur = self._standard_login_request(invalid_username, invalid_password)
        self.assertEqual(bur.status_code, 400)
        bur_data = json.loads(bur.data)
        #bur assertions
        self.assertFalse(bur_data.get('success'))
        self.assertEqual(bur_data.get('response').get('error'), 'StandardAuthFailure')
        # Now verify the responses are identical
        self.assertEqual(bpr_data, bur_data)

    # /api/buildings tests

    def test_list_buildings_okay(self):
        num_expected_results = 9
        bearer_token = self._standard_login()
        result = self.client.get('/api/buildings', headers={'Authorization': bearer_token})
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertTrue(data.get('success'))
        self.assertEqual(len(data.get('response')), num_expected_results)

    def test_list_buildings_unauthed(self):
        result = self.client.get('/api/buildings')
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertFalse(data.get('success'))
        self.assertEqual(data.get('response').get('error'), 'MissingRequiredHeader')

    def test_list_buildings_public_only(self):
        """ Test user cannot see buildings owned by other accounts that are not marked public """
        bearer_token = self._standard_login()
        result = self.client.get('/api/buildings', headers={'Authorization': bearer_token})
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        for i in data.get('response'):
            self.assertIn(i['owner_id'], [PUBLIC_USER_ID])

    # /api/buildings/<id> tests

    def test_get_building_okay(self):
        """ Test user can get a public building successfully """
        building_id = 1
        bearer_token = self._standard_login()
        result = self.client.get('/api/buildings/{}'.format(building_id), headers={'Authorization': bearer_token})
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        response = data.get('response')
        self.assertTrue(data.get('success'))
        self.assertIn('id', response.keys())
        self.assertEqual(response.get('id'), building_id)
        self.assertEqual(response.get('owner_id'), PUBLIC_USER_ID)
        self.assertTrue(response.get('is_public'))

    def test_get_building_unauthed(self):
        """ Test user cannot get public building without being authenticated """
        building_id = 1
        result = self.client.get('/api/buildings/{}'.format(building_id))
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertFalse(data.get('success'))
        self.assertEqual(data.get('response').get('error'), 'MissingRequiredHeader')

    def test_get_building_not_public_not_owned(self):
        """ Test user cannot get a private building owned by another user """
        building_id = 11
        bearer_token = self._standard_login()
        result = self.client.get('/api/buildings/{}'.format(building_id), headers={'Authorization': bearer_token})
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertFalse(data.get('success'))
        self.assertEqual(data.get('response').get('error'), 'ItemNotFound')

    def test_get_building_not_public_is_owned(self):
        """ Test user can get private building owned by themselves """
        building_id = 11
        owner_id = 2
        username = 'tina'
        password = 'zombies'
        bearer_token = self._standard_login(username=username, password=password)
        result = self.client.get('/api/buildings/{}'.format(building_id), headers={'Authorization': bearer_token})
        response = json.loads(result.data).get('response')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(response.get('id'), building_id)
        self.assertEqual(response.get('owner_id'), owner_id)
        self.assertFalse(response.get('is_public'))
