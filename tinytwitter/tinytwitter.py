#coding: utf8

import oauth2 as oauth
import time
import urllib
import urllib2
import base64

class TwitterError(Exception):
    pass

CONVERT = lambda x: json.loads(x)
NOT_CONVERT = lambda x: x

class Auth(object):
    def generate_request(self, url, method, params):
        raise NotImplementedError()
    
    def choose_method(self, url, method, params):
        if method == 'GET':
            request = urllib2.Request('%s?%s' % (url, urllib.urlencode(params)))
        else:
            request = urllib2.Request(url, data=urllib.urlencode(params))
            if method == 'POST':
                pass
            elif method == 'PUT':
                request.get_method = lambda: 'PUT'
            elif method == 'DELETE':
                request.get_method = lambda: 'DELETE'
            else:
                raise TwitterError('There is not the method called %s' % method)
        return request
        
class NoAuth(Auth):
    def generate_request(self, url, method, params):
        return self.choose_method(url, method, params)

class BasicAuth(Auth):
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def generate_request(self, url, method, params):
        request = self.choose_method(url, method, params)
        basic = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
        request.add_header('Authorization', 'Basic %s' % basic)
        return request

class OAuth(Auth):
    def __init__(self, consumer_key, consumer_secret, token_key=None, token_secret=None):
        self.consumer = oauth.Consumer(consumer_key, consumer_secret)
        if token_key is not None and token_secret is not None:
            self.token = oauth.Token(token_key, token_secret)
    
    def generate_request(self, url, method, params):
        oauth_params = {
            'oauth_version': '1.0',
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time()),
            'oauth_token': self.token.key,
            'oauth_consumer_key': self.consumer.key,
        }
        oauth_params.update(params)
        oauth_request = oauth.Request(method=method, url=url, parameters=oauth_params)
        oauth_request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.consumer, self.token)
        request = self.choose_method(url, method, params)
        request.add_header('Authorization', oauth_request.to_header()['Authorization'])
        return request

class Api(object):
    def __init__(self, auth=None, convert_to_dict=True):
        self._auth = auth or NoAuth()
        self.convert = CONVERT if convert_to_dict else NOT_CONVERT
    
    def raw_response(self, url, method, **params):
        return urllib2.urlopen(self._auth.generate_request(url, method, params))
    
    def fetch(self, url, method, **params):
        return self.convert(self.raw_response(url, method, **params).read())
    
    def get(self, url, **params):
        return self.fetch(url, 'GET', **params)
    
    def post(self, url, **params):
        return self.fetch(url, 'POST', **params)
    
    def put(self, url, **params):
        return self.fetch(url, 'PUT', **params)
    
    def delete(self, url, **params):
        return self.fetch(url, 'DELETE', **params)
    
    def stream(self, url, method, fn, **params):
        res = self.raw_response(url, method, **params)
        for line in res:
            fn(self.convert(line))
