import requests
import xml.etree.ElementTree as ET


#"http://finance.yahoo.com/d/quotes.csv?s=AAPL+GOOG+MSFT&f=nab"


stocks = ['GOOG', 'AAPL', 'IBM', 'ORCL']
data_req = "snlabp2gh" #http://www.jarloo.com/yahoo_finance/

base_url = "http://finance.yahoo.com/d/quotes.csv?"
stocks_url = base_url + "s=" + "+".join(stocks)
req_url = stocks_url + "&f=" + data_req
r = requests.get(req_url)

for stock in stocks:
    url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s={}&region=US&lang=en-US".format(stock)
    r = requests.get(url)
    tree = ET.fromstring(r.text)

    print tree






print r.text