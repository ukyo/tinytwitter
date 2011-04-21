#coding: utf8

import oauth2 as oauth
import time
import urllib
import urllib2
import base64

'''
Example:
    >>> #normal api
    >>> import tinytwitter as twitter
    >>> consumer_key = 'your-consumer-key'
    >>> consumer_secret = 'your-consumer-secret'
    >>> token_key = 'token-key'
    >>> token_secret = 'token-secret'
    >>> auth = OAuth(consumer_key, consumer_secret, token_key, token_secret)
    >>> api = twitter.Api(auth)
    >>> api.fetch('http://api.twitter.com/1/1/statuses/update.json', 'POST', status='test message')
    >>> #streaming api
    >>> def print_tweet(tweet):
    >>>     try:
    >>>         print tweet['user']['screen_name'], tweet['text']
    >>>     except:
    >>>         pass
    >>> api.stream('http://stream.twitter.com/1/statuses/sample.json', 'GET', print_tweet)
'''

try:
    'python 2.6 or later'
    import json
except:
    try:
        'python 2.5 or before'
        import simplejson as json
    except:
        try:
            'Google App Engine'
            import django.utils.simplejson as json
        except:
            raise ImportError('Require simplejson.')

#search api
SEARCH = 'http://search.twitter.com/search.json'

#timeline resources
STATUSES_PUBLIC_TIMELIME = 'http://api.twitter.com/1/statuses/public_timeline.json'
STATUSES_HOME_TIMELINE = 'http://api.twitter.com/1/statuses/home_timeline.json'
STATUSES_FRIENDS_TIMELINE = 'http://api.twitter.com/1/statuses/friends_timeline.json'
STATUSES_USER_TIMELINE = 'http://api.twitter.com/1/statuses/user_timeline.json'
STATUSES_MENTIONS = 'http://api.twitter.com/1/statuses/mentions.json'
STATUSES_RETWEETED_BY_ME = 'http://api.twitter.com/1/statuses/retweeted_by_me.json'
STATUSES_RETWEETED_TO_ME = 'http://api.twitter.com/1/statuses/retweeted_to_me.json'
STATUSES_RETWEETS_OF_ME = 'http://api.twitter.com/1/statuses/retweets_of_me.json'

#tweets resouces
STATUSES_SHOW_ID = 'http://api.twitter.com/1/statuses/show/%d.json'
STATUSES_UPDATE = 'http://api.twitter.com/1/statuses/update.json'
STATUSES_DESTROY_ID = 'http://api.twitter.com/1/statuses/destroy/%d.json'
STATUSES_RETWEET_ID = 'http://api.twitter.com/1/statuses/retweet/%d.json'
STATUSES_RETWEETS_ID = 'http://api.twitter.com/1/statuses/retweets/%d.json'
STATUSES_ID_RETWEETED_BY = 'http://api.twitter.com/1/statuses/%d/retweeted_by.json'
STATUSES_ID_RETWEETED_BY_IDS = 'http://api.twitter.com/1/statuses/%d/retweeted_by_ids.json'

#user resouces
USERS_SHOW = 'http://api.twitter.com/1/users/show.json'
USERS_LOOLUP = 'http://api.twitter.com/1/users/lookup.json'
USERS_SEACH = 'http://api.twitter.com/1/users/search.json'
USERS_SUGGESTIONS = 'http://api.twitter.com/1/users/suggestions.json'
USERS_SUGGESTIONS_TWITTER ='http://api.twitter.com/1/users/suggestions/twitter.json'
USERS_PROFILE_IMAGE_TWITTER = 'http://api.twitter.com/1/users/profile_image/twitter.json'
STATUSES_FRIENDS = 'http://api.twitter.com/1/statuses/friends.json'
STATUSES_FOLLOWERS = 'http://api.twitter.com/1/statuses/followers.json'

#trend resouces
TRENDS = 'http://api.twitter.com/1/trends.json'
TRENDS_CURRENT = 'http://api.twitter.com/1/trends/current.json'
TRENDS_DAIRY = 'http://api.twitter.com/1/trends/dairy.json'
TRENDS_WEEKLY = 'http://api.twitter.com/1/trends/weekly.json'

#local trends resouces
TRENDS_AVAILABLE = 'http://api.twitter.com/1/trends/availabale.json'
TRENDS_WOEID = 'http://api.twitter.com/1/%d.json'

#list resources
USER_LISTS = 'http://api.twitter.com/1/%s/lists.json'
USER_LISTS_ID = 'http://api.twitter.com/1/%s/lists/%d.json'
USER_LISTS_ID_STATUSES = 'http://api.twitter.com/1/%s/lists/%d/statuses.json'
USER_LISTS_MEMBERSHIPS = 'http://api.twitter.com/1/%s/lists/memberships.json'
USER_LISTS_SUBSCRIPTIONS = 'http://api.twitter.com/1/%s/lists/subscriptions.json'

#list members resources
USER_LIST_ID_MEMBERS = 'http://api.twitter.com/1/%s/%d/members.json'
USER_LIST_ID_CREATE_ALL = 'http://api.twitter.com/1/%s/%d/create_all.json'
USER_LIST_ID_MEMBERS_ID = 'http://api.twitter.com/1/%s/%d/members/%d.json'

#list subscribers resources
USER_LIST_ID_SUBSCRIBERS = 'http://api.twitter.com/1/%s/%d/subscribers.json'
USER_LIST_ID_SUBSCRIBERS_UD = 'http://api.twitter.com/1/%d/%d/subscribers/%d.json'

#direct messages rewources
DIRECT_MESSAGES = 'http://api.twitter.com/1/direct_messages.json'
DIRECT_MESSAGES_SENT = 'http://api.twitter.com/1/direct_messages/sent.json'
DIRECT_MESSAGES_NEW = 'http://api.twitter.com/1/direct_messages/new.json'
DIRECT_MESSAGES_DESTROY_ID = 'http://api.twitter.com/1/direct_messages/destroy/%d.json'

#friendship resources
FRIENDSHIPS_CREATE = 'http://api.twitter.com/1/friendships/create.json'
FRIENDSHIPS_DESTROY = 'http://api.twitter.com/1/friendships/destroy.json'
FRIENDSHIPS_EXISTS = 'http://api.twitter.com/1/friendships/exists.json'
FRIENDSHIPS_SHOW = 'http://api.twitter.com/1/friendships/show.json'
FRIENDSHIPS_INCOMING = 'http://api.twitter.com/1/friendships/incoming.json'
FRIENDSHIPS_OUTGOING = 'http://api.twitter.com/1/friendships/outgoing.json'

#friends and followers resouces
FRIENDS_IDS = 'http://api.twitter.com/1/friends/ids.json'
FOLLOWERS_IDS = 'http://api.twitter.com/1/followers/ids.json'

#account resources
ACCOUNT_VERIFY_CREDENTIALS = 'http://api.twitter.com/1/account/verify_credentials.json'
ACCOUNT_RATE_LIMIT_STATUS = 'http://api.twitter.com/1/account/rate_limit_status.json'
ACCOUNT_END_SESSION = 'http://api.twitter.com/1/account/end_session.json'
ACCOUNT_UPDATE_DELIVERY_DEVICE = 'http://api.twitter.com/1/account/update_delivery_device.json'
ACCOUNT_UPDATE_PROFILE_COLORS = 'http://api.twitter.com/1/account/update_profile_colors.json'
ACCOUNT_UPDATE_PROFILE_IMAGE = 'http://api.twitter.com/1/account/update_profile_image.json'
ACCOUNT_UPDATE_PROFILE_BACKGROUND_IMAGE = 'http://api.twitter.com/1/account/update_profile_background_image.json'
ACCOUNT_UPDATE_PROFILE = 'http://api.twitter.com/1/account/update_profile.json'

#favorites resources
FAVORITES = 'http://api.twitter.com/1/favorites.json'
FAVORITES_CREATE_ID = 'http://api.twitter.com/1/favorites/create/%d.json'
FAVORITES_DESTROY_ID = 'http://api.twitter.com/1/favorites/destroy/%d.json'

#notification rewources
NOTIFICATIONS_FOLLOW = 'http://api.twitter.com/1/notifications/follow.json'
NOTIFICATIONS_LEAVE = 'http://api.twitter.com/1/notifications/leave.json'

#block resources
BLOCKS_CREATE = 'http://api.twitter.com/1/blocks/create.json'
BLOCKS_DESTROY = 'http://api.twitter.com/1/blocks/destroy.json'
BLOCKS_EXISTS = 'http://api.twitter.com/1/blocks/exists.json'
BLOCKS_BLOCKING = 'http://api.twitter.com/1/blocks/blocking.json'
BLOCKS_BLOCKING = 'http://api.twitter.com/1/blocks/blocking/ids.json'

#spam reporting resources
REPORT_SPAM = 'http://api.twitter.com/1/report_spam.json'

#saved searches resources
SAVED_SEARCHES = 'http://api.twitter.com/1/saved_searches.json'
SAVED_SEARCHES_SHOW_ID = 'http://api.twitter.com/1/saved_searches/show/%d.json'
SAVED_SEARCHES_CREATE = 'http://api.twitter.com/1/saved_searches/create.json'
SAVED_SEARCHES_DESTROY_ID = 'http://api.twitter.com/1/saved_searches/destroy/%d.json'

#geo resources
GEO_NEARBY_PLACES = 'http://api.twitter.com/1/geo/nearby_places.json'
GEO_SEARCH = 'http://api.twitter.com/1/geo/search.json'
GEO_SIMILAR_PLACES = 'http://api.twitter.com/1/geo/similar_places.json'
GEO_REVERSE_GEOCODE = 'http://api.twitter.com/1/geo/reverse_geocode.json'
GEO_ID_PLACE_ID = 'http://api.twitter.com/1/geo/id/%d.json'
GEO_PLACE = 'http://api.twitter.com/1/geo/place.json'

#legal resources
LEGAL_TOS = 'http://api.twitter.com/1/legal/tos.json'
LEGAL_PRIVACY = 'http://api.twitter.com/1/legal/privacy.json'

#help resources
HELP_TEST = 'http://api.twitter.com/1/help/test.json'

#stream api
STREAM_FILTER = 'http://stream.twitter.com/1/statuses/filter.json'
STREAM_FIREHOSE = 'http://stream.twitter.com/1/statuses/firehose.json'
STREAM_LINKS = 'http://stream.twitter.com/1/statuses/links.json'
STREAM_RETWEET = 'http://stream.twitter.com/1/statuses/retweet.json'
STREAM_SAMPLE = 'http://stream.twitter.com/1/statuses/sample.json'
STREAM_USER = 'https://userstream.twitter.com/2/user.json'

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
    def __init__(self, auth, convert_to_dict=True):
        self._auth = auth
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
