# pyknowsis
A python client for the Knowsis API

```python

from pyknowsis import KnowsisClient

client = KnowsisClient('consumer_key', 'consumer_secret')

client.assets(page=10, pagesize=5)

client.asset("AAPL")

client.asset_sentiment("AAPL")

```
