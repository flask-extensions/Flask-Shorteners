# coding: utf-8
import json

import requests

from .utils import is_valid_url

__all__ = ['GoogleShortener', 'BitlyShortener']

class BaseShortener(object):
    def __init__(self, url, app=None):
        self.url = url

        if app is not None:
            self.app = app

        if isinstance(url, unicode):
            self.url = url.encode('utf-8')

        if not is_valid_url(self.url):
            raise ValueError(u'Please enter a valid url')

    def init_app(self, app, **kwargs):
        app.config.update(kwargs)

    def short(self):
        """
        Method used to short url
        """
        raise NotImplementedError()

    def expand(self):
        """
        Method used to unshort url
        """
        raise NotImplementedError()


class GoogleShortener(BaseShortener):
    """
    Based on:
    https://github.com/avelino/django-googl/blob/master/googl/short.py
    Googl Shortener Implementation
    Doesn't need anything from the app

    """
    api_url = "https://www.googleapis.com/urlshortener/v1/url"

    def short(self):
        params = json.dumps({'longUrl': self.url})
        headers = {'content-type': 'application/json'}
        response = requests.post(self.api_url, data=params,
                                 headers=headers)
        if response.ok:
            data = response.json()
            if 'id' in data:
                self.shorten = data['id']
                return data['id']
        return u''

    def expand(self):
        params = {'shortUrl': self.url}
        response = requests.get(self.api_url, params=params)
        if response.ok:
            data = response.json()
            if 'longUrl' in data:
                return data['longUrl']
        return u''


class BitlyShortener(BaseShortener):
    """
    Bit.ly shortener Implementation
    needs on app.config:
    BITLY_LOGIN - Your bit.ly login user
    BITLY_API_KEY - Your bit.ly api key
    """
    shorten_url = 'http://api.bit.ly/shorten'
    expand_url = 'http://api.bit.ly/expand'

    def __init__(self, url, *args, **kwargs):
        if not kwargs.get('app'):
            raise ValueError(u'You must pass an app instance on Bit.ly'
                             u'shortener')

        app = kwargs.get('app')
        if not app.config.get('BITLY_LOGIN') and \
           not app.config.get('BITLY_API_KEY'):
            return None

        self.login = app.config.get('BITLY_LOGIN')
        self.api_key = app.config.get('BITLY_API_KEY')

        super(BitlyShortener, self).__init__(url, *args, **kwargs)

    def short(self):
        params = dict(
            version="2.0.1",
            longUrl=self.url,
            login=self.login,
            apiKey=self.api_key,
        )
        response = requests.post(self.shorten_url, data=params)
        if response.ok:
            data = response.json()
            if 'statusCode' in data and data['statusCode'] == 'OK':
                key = self.url
                return data['results'][key]['shortUrl']
        return u''

    def expand(self):
        params = dict(
            version="2.0.1",
            shortUrl=self.url,
            login=self.login,
            apiKey=self.api_key,
        )
        response = requests.get(self.expand_url, params=params)
        if response.ok:
            data = response.json()
            if 'statusCode' in data and data['statusCode'] == 'OK':
                # get the hash key that contains the longUrl
                hash_key = data['results'].keys()[0]
                return data['results'][hash_key]['longUrl']
        return u''
