"""
Tests for Docebo backend.
"""
import json

import requests
from social_core.tests.backends.oauth import OAuth2Test


class OktaOAuth2Test(OAuth2Test):
    """
    Tests for the Docebo social auth backed
    """
    backend_path = 'social_auth_backend_docebo.backend.DoceboOAuth2'
    user_data_url = 'https://testing.docebosaas.com/manage/v1/user/session'
    expected_username = 'foo'
    access_token_body = json.dumps({
        'access_token': 'foobar',
        'token_type': 'bearer'
    })
    user_data_body = json.dumps({
        "data": {
            "id": 11234,
            "username": "foo",
            "firstname": "Foo",
            "lastname": "Bar",
            "email": "foo.bar@example.com",
            "avatar_url": "https://some.site/path/to/avatar.png",
        }
    })

    def test_login(self):
        self.strategy.set_settings({
            'DOMAIN': 'testing.docebosaas.com'
        })
        self.do_login()

    def test_partial_pipeline(self):
        self.strategy.set_settings({
            'DOMAIN': 'testing.docebosaas.com'
        })
        self.do_partial_pipeline()

    def test_get_user_details(self):
        self.strategy.set_settings({
            'DOMAIN': 'testing.docebosaas.com'
        })
        user = self.do_partial_pipeline()
        assert user.email == 'foo.bar@example.com'
        response = requests.get(self.user_data_url)
        user_details = self.backend.get_user_details(
            response.json()['data']
        )
        self.assertEqual(user_details['email'], 'foo.bar@example.com')
        self.assertEqual(user_details['username'], 'foo')
        self.assertEqual(user_details['name'], 'Foo Bar')
        self.assertEqual(user_details['first_name'], 'Foo')
        self.assertEqual(user_details['last_name'], 'Bar')
        self.assertEqual(user_details['user_id'], 11234)
        self.assertEqual(user_details['picture'], "https://some.site/path/to/avatar.png")
