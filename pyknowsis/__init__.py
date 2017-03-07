import urlparse
import time
from datetime import datetime
from dateutil.parser import parse as dateparse
import oauth2 as oauth
import requests

default_headers = {'Accept': 'application/json', 'Connection': 'close'}

base_uri = 'https://api.knows.is'


def create_identifiers(identifiers):

    return [
        Identifier(identifier.get('identifier'), identifier.get('type'))
        for identifier
        in identifiers
    ]



def create_asset(asset_json):
    name = asset_json.get('name')
    identifiers = create_identifiers(asset_json.get('identifiers'))

    return Asset(asset_name=name, asset_identifiers=identifiers,
                 asset_type=None)


def create_meta(json):
    return Meta(json.get('page'), json.get('pagesize'), json.get('items'),
                json.get('total_items'))


def create_sentiment(sentiment_json):
    current = sentiment_json.get('current')
    previous = sentiment_json.get('previous')
    change = sentiment_json.get('change')

    return Sentiment(current, previous, change)


def create_volume(volume_json):
    current = volume_json.get('current')
    previous = volume_json.get('previous')
    change = volume_json.get('change')

    return Volume(current, previous, change)


def create_counts(counts_json):
    positive = counts_json.get('positive')
    negative = counts_json.get('negative')
    neutral = counts_json.get('neutral')
    total = counts_json.get('total')

    return Counts(positive, negative, neutral, total)


def create_datapoint(datapoint_json):
    date = datetime.strptime(datapoint_json.get('date'), "%Y-%m-%dT%H:%M:%S")
    sentiment = create_sentiment(datapoint_json.get('sentiment', {}))
    volume = create_volume(datapoint_json.get('volume', {}))

    counts = create_counts(datapoint_json.get("tweet_counts", {}))

    return SentimentDatapoints(
        date=date, sentiment=sentiment, volume=volume, counts=counts)


def create_asset_sentiment(asset_sentiment_json):
    name = asset_sentiment_json.get('name')
    identifier = asset_sentiment_json.get('identifer')

    startdate = datetime.strptime(
        asset_sentiment_json.get('startdate'), "%Y-%m-%dT%H:%M:%S")
    enddate = datetime.strptime(
        asset_sentiment_json.get('enddate'),"%Y-%m-%dT%H:%M:%S")

    datapoints = [
        create_datapoint(dp)
        for dp
        in asset_sentiment_json.get('datapoints')
    ]

    return AssetSentiment(name, identifier, startdate, enddate, datapoints)


def create_price_datapoint(datapoint_json):
    date = dateparse(datapoint_json.get('date'))
    high = datapoint_json.get('high', {})
    low = datapoint_json.get('low', {})
    open = datapoint_json.get('open', {})
    close = datapoint_json.get('close', {})
    adj_close = datapoint_json.get('adj_close', {})
    last = datapoint_json.get('last', {})
    volume = datapoint_json.get('volume', {})

    return PriceDatapoint(date=date, high=high, low=low, open=open, close=close,
                          adj_close=adj_close, last=last, volume=volume)


class AssetPricing(object):
    def __init__(self, name, identifier, startdate, enddate, datapoints):
        self.pricing = datapoints
        self.enddate = enddate
        self.startdate = startdate
        self.identifier = identifier
        self.name = name


def create_asset_pricing(asset_pricing_json):
    name = asset_pricing_json.get('name')
    identifier = asset_pricing_json.get('identifer')

    startdate = datetime.strptime(asset_pricing_json.get('startdate'),
                                  "%Y-%m-%dT%H:%M:%S")
    enddate = datetime.strptime(asset_pricing_json.get('enddate'),
                                "%Y-%m-%dT%H:%M:%S")

    datapoints = [create_price_datapoint(datapoint) for datapoint in
                  asset_pricing_json.get('pricing')]


    return AssetPricing(name, identifier, startdate, enddate, datapoints)


class KnowsisClient(object):
    def __init__(self, oauth_consumer_key, oauth_consumer_secret):

        self.oauth_consumer_key = oauth_consumer_key
        self.oauth_consumer_secret = oauth_consumer_secret

    def _get_response_for_signed_request(
            self, url, headers={}, querystring=None, use_https=False):

        request_headers = default_headers

        request_headers['User-Agent'] = 'pyknowsis'
        request_headers['From'] = self.oauth_consumer_key

        if headers:
            request_headers.update(headers)

        url = urlparse.urljoin(base_uri, url)

        if use_https:
            url = url.replace('http', 'https')

        request_url = self._generate_valid_signed_request_url(
            url, 'GET', querystring=querystring)


        attempts = 0

        while attempts < 3:
            try:
                resp = requests.get(request_url, headers=request_headers)

                return resp
            except Exception as ex:
                pass

            attempts += 1

    def _generate_valid_signed_request_url(
            self, url, method='GET', querystring={}):

        consumer = oauth.Consumer(
            self.oauth_consumer_key, self.oauth_consumer_secret)

        oauth_params = {
            'oauth_version': '1.0',
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time())
        }

        if querystring:
            oauth_params.update(querystring)

        signature_method = oauth.SignatureMethod_HMAC_SHA1()

        request = oauth.Request(method=method, url=url, parameters=oauth_params)
        request.sign_request(signature_method, consumer, None)

        signed_querystring = urlparse.urlparse(request.to_url())[4]
        return '{0}?{1}'.format(url, signed_querystring)

    def asset_list(self, url, page=None, pagesize=None):

        querystring = dict()

        if page:
            querystring['page'] = page
        if pagesize:
            querystring['pagesize'] = pagesize

        if pagesize > 100:
            raise ValueError("Pagesize cannot be greater than 100")

        response = self._get_response_for_signed_request(
            url, querystring=querystring,
            headers={'Accept': 'application/json'})

        if response.status_code == 200:
            meta = create_meta(response.json().get('meta'))

            assets = [
                create_asset(asset)
                for asset
                in response.json().get('assets')
            ]

            return AssetList(meta, assets)

        raise Exception(response.content)

    def assets(self, page=None, pagesize=None):

        url = '/assets/'

        return self.asset_list(url, page, pagesize)

    def equities(self, page=None, pagesize=None):

        url = '/equities/'

        return self.asset_list(url, page, pagesize)

    def indices(self, page=None, pagesize=None):

        url = '/indices/'

        return self.asset_list(url, page, pagesize)

    def commodities(self, page=None, pagesize=None):
        url = '/commodities/'

        return self.asset_list(url, page, pagesize)

    def forex(self, page=None, pagesize=None):
        url = '/forex/'

        return self.asset_list(url, page, pagesize)

    def bonds(self, page=None, pagesize=None):
        url = '/bonds/'

        return self.asset_list(url, page, pagesize)

    def etfs(self, page=None, pagesize=None):
        url = '/etfs/'

        return self.asset_list(url, page, pagesize)

    def asset(self, identifier):

        url = '/assets/{0}/'.format(identifier)

        response = self._get_response_for_signed_request(
            url, headers={'Accept': 'application/json'})

        if response.status_code == 200:
            return create_asset(response.json())

        raise Exception(response.content)

    def asset_intraday_sentiment(
            self, identifier, startdate=None, enddate=None, sparse=False):

        url = '/assets/{0}/intraday/'.format(identifier)
        querystring = {}

        if startdate:
            querystring['startdate'] = startdate.strftime("%Y%m%d%H%M")

        if enddate:
            querystring['enddate'] = enddate.strftime("%Y%m%d%H%M")

        querystring['sparse'] = sparse

        response = self._get_response_for_signed_request(
            url, querystring=querystring,
            headers={'Accept': 'application/json'}
        )

        if response.status_code == 200:
            return create_asset_sentiment(response.json())

        raise Exception(response.content)

    def asset_sentiment(
            self, identifier, startdate=None, enddate=None, sparse=False):

        url = '/assets/{0}/sentiment/'.format(identifier)

        querystring = {}

        if startdate:
            querystring['startdate'] = startdate.strftime("%Y%m%d%H%M")

        if enddate:
            querystring['enddate'] = enddate.strftime("%Y%m%d%H%M")

        querystring['sparse'] = sparse

        response = self._get_response_for_signed_request(
            url, querystring=querystring,
            headers={'Accept': 'application/json'})

        if response.status_code == 200:
            return create_asset_sentiment(response.json())

        raise Exception(response.content)

    def asset_themes(self, identifier):

        url = '/assets/{0}/themes/'.format(identifier)

        response = self._get_response_for_signed_request(url, headers={
            'Accept': 'application/json'})

        return response.json()

    def asset_pricing(self, identifier, startdate=None, enddate=None):

        url = '/assets/{0}/pricing/'.format(identifier)

        querystring = {}

        if startdate:
            querystring['startdate'] = startdate.strftime("%Y%m%d")

        if enddate:
            querystring['enddate'] = enddate.strftime("%Y%m%d")

        response = self._get_response_for_signed_request(
            url, querystring=querystring,
            headers={'Accept': 'application/json'})

        if response.status_code == 200:
            return create_asset_pricing(response.json())

        raise Exception(response.content)

    def asset_tweets(self, identifier):

        url = '/assets/{0}/tweets/'.format(identifier)

        response = self._get_response_for_signed_request(url, headers={
            'Accept': 'application/json'})

        return response.json()


class AssetList:

    def __init__(self, meta, assets):
        self.assets = assets
        self.meta = meta

    def __repr__(self):
        return str(self.__dict__)


class Asset:

    def __init__(self, asset_name, asset_identifiers, asset_type):
        self.type = asset_type
        self.identifiers = asset_identifiers
        self.name = asset_name

    def __repr__(self):
        return str(self.__dict__)


class AssetSentiment:

    def __init__(self, name, identifier, startdate, enddate, datapoints):
        self.datapoints = datapoints
        self.enddate = enddate
        self.startdate = startdate
        self.name = name
        self.identifier = identifier

    def __repr__(self):
        return str(self.__dict__)


class SentimentDatapoints:
    def __init__(self, date, sentiment, volume, counts):
        self.volume = volume
        self.sentiment = sentiment
        self.counts = counts
        self.date = date

    def __repr__(self):
        return str(self.__dict__)


class Counts:
    def __init__(self, positive, negative, neutral, total):
        self.positive = positive
        self.negative = negative
        self.neutral = neutral
        self.total = total

    def __repr__(self):
        return str(self.__dict__)


class Sentiment:

    def __init__(self, current, previous, change):
        self.change = change
        self.previous = previous
        self.current = current

    def __repr__(self):
        return str(self.__dict__)


class Volume:

    def __init__(self, current, previous, change):
        self.change = change
        self.previous = previous
        self.current = current

    def __repr__(self):
        return str(self.__dict__)


class Meta:

    def __init__(self, page, pagesize, items, total_items):
        self.total_items = total_items
        self.items = items
        self.pagesize = pagesize
        self.page = page

    def __repr__(self):
        return str(self.__dict__)


class Identifier:

    def __init__(self, identifier, type):
        self.type = type
        self.identifier = identifier

    def __repr__(self):
        return str(self.__dict__)


class KnowsisAPIError(Exception):
    def __init__(self, args, kwargs):
        super(KnowsisAPIError, self).__init__(*args, **kwargs)


class PriceDatapoint(object):
    def __init__(self, date, high, low, open, close, adj_close, last, volume):
        self.volume = volume
        self.last = last
        self.adj_close = adj_close
        self.close = close
        self.open = open
        self.low = low
        self.high = high
        self.date = date

    def __repr__(self):

        return str(self.__dict__)

