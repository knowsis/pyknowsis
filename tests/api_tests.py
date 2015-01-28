from datetime import datetime, time
import unittest

from pyknowsis import KnowsisClient, Identifier

oauth_consumer_key = ""
oauth_consumer_secret =""


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

        self.assertEqual(asset.asset_name, "Apple Inc")
        self.assertIsInstance(asset.asset_identifiers, list)
        self.assertIsInstance(asset.asset_identifiers[0], Identifier)



class TestAssetSentimentEndpoint(unittest.TestCase):

    def test_returns_correct_asset(self):

        api = KnowsisClient(oauth_consumer_key, oauth_consumer_secret)

        asset = api.asset_sentiment(identifier="AAPL")

        self.assertEqual(asset.name, "Apple Inc")
        self.assertEqual(asset.startdate,  datetime.combine(datetime.utcnow(), time.min))

