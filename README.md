# pyknowsis
A python client for the Knowsis API

```python
from pyknowsis import KnowsisClient
```

Create a Knowsis API client

```python
knowsis = KnowsisClient('consumer_key', 'consumer_secret')
```

Get a list of assets, this list will return a max of 100 assets at a time and can be paged.
```python
knowsis.assets(page=10, pagesize=5)
```

Get the details of a single asset
```python
knowsis.asset("AAPL")
```

Get the daily sentiment for an asset.
By default this will return the sentiment for the current day only, but a range can be selected by using the startdate and enddate parameter
```python
knowsis.asset_sentiment("AAPL", startdate=datetime(2015,01,01), enddate=datetime(2015,01,03))
```

Get the intraday sentiment for an asset.
By default this will return the sentiment for the last period only, but a range can be selected by using the startdate and enddate parameters
```python
knowsis.asset_intraday_sentiment("AAPL",startdate=datetime(2015,01,01,08,00), enddate=datetime(2015,01,01,12,00))
```




