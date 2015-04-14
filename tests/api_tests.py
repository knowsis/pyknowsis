from datetime import datetime, time, timedelta
import unittest
import os

from pyknowsis import KnowsisClient, Identifier

oauth_consumer_key = os.environ.get("KNOWSIS_API_CONSUMER_KEY")
oauth_consumer_secret = os.environ.get("KNOWSIS_API_CONSUMER_SECRET")


class TestAssetsEndpoint(unittest.TestCase):

    def test_returns_correct_meta(self):

        api = KnowsisClient(oauth_consumer_key, oauth_consumer_secret)

        page = 2
        pagesize = 5
        assets = api.assets(page=page, pagesize=pagesize)

        self.assertIsNotNone(assets.assets)
        self.assertEqual(assets.meta.page, page)
        self.assertEqual(assets.meta.pagesize, pagesize)
        self.assertIsNotNone(assets.assets)
        self.assertIsInstance(assets.assets, list)

        self.assertEqual(len(assets.assets), assets.meta.items)


class TestAssetEndpoint(unittest.TestCase):

    def test_returns_correct_asset(self):

        api = KnowsisClient(oauth_consumer_key, oauth_consumer_secret)

        asset = api.asset(identifier="AAPL")

        self.assertEqual(asset.name, "Apple Inc")
        self.assertIsInstance(asset.identifiers, list)
        self.assertIsInstance(asset.identifiers[0], Identifier)


class TestAssetSentimentEndpoint(unittest.TestCase):

    def test_returns_correct_asset(self):

        api = KnowsisClient(oauth_consumer_key, oauth_consumer_secret)

        asset = api.asset_sentiment(identifier="AAPL")

        self.assertEqual(asset.name, "Apple Inc")

    def test_returns_data_for_last_period_by_default(self):

        api = KnowsisClient(oauth_consumer_key, oauth_consumer_secret)

        asset = api.asset_sentiment(identifier="AAPL")

        current_day = datetime.combine(datetime.utcnow(), time.min)

        self.assertEqual(asset.name, "Apple Inc")
        self.assertEqual(asset.startdate, current_day)
        self.assertEqual(asset.enddate,  current_day)

    def test_returns_data_for_daterange_specified(self):

        api = KnowsisClient(oauth_consumer_key, oauth_consumer_secret)
        startdate = datetime.combine(datetime.utcnow(), time.min) - timedelta(days=5)
        enddate = datetime.combine(datetime.utcnow(), time.min) - timedelta(days=2)

        asset = api.asset_sentiment(identifier="AAPL", startdate=startdate, enddate=enddate)

        self.assertEqual(asset.name, "Apple Inc")
        self.assertEqual(asset.startdate,  startdate)
        self.assertEqual(asset.enddate,  enddate)


class TestAssetIntradaySentimentEndpoint(unittest.TestCase):

    def test_returns_correct_asset(self):

        api = KnowsisClient(oauth_consumer_key, oauth_consumer_secret)

        asset = api.asset_intraday_sentiment(identifier="AAPL")

        self.assertEqual(asset.name, "Apple Inc")

    def test_returns_data_for_current_day_by_default(self):

        api = KnowsisClient(oauth_consumer_key, oauth_consumer_secret)

        asset = api.asset_intraday_sentiment(identifier="AAPL")

        now = datetime.utcnow()
        last_period = now - timedelta(minutes=now.minute % 5, seconds=now.second, microseconds=now.microsecond)

        self.assertEqual(asset.name, "Apple Inc")
        self.assertEqual(asset.startdate,  last_period)
        self.assertEqual(asset.enddate,  last_period)

    def test_returns_data_for_daterange_specified(self):

        api = KnowsisClient(oauth_consumer_key, oauth_consumer_secret)

        startdate = datetime.combine(datetime.utcnow(), time.min)
        enddate = datetime.combine(datetime.utcnow(), time.min) + timedelta(hours=6)

        asset = api.asset_intraday_sentiment(identifier="AAPL", startdate=startdate, enddate=enddate)

        self.assertEqual(asset.name, "Apple Inc")
        self.assertEqual(asset.startdate,  startdate)
        self.assertEqual(asset.enddate,  enddate)