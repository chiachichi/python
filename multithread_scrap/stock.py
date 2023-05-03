import threading
import requests
from lxml import html


class Stock(threading.Thread):
    '''Scraps multithreaded the stock prices from the Yahoo Finance website.
    
    Inputs:
    - symbol(str): company name

    Usage Example:

    symbols = ['MSFT', 'GOOGL', 'AAPL', 'META']
    threads = []

    for symbol in symbols:
        t = Stock(symbol)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
        print(t)
    '''
    def __init__(self, symbol: str) -> None:
        super().__init__()

        self.symbol = symbol
        self.url = f'https://finance.yahoo.com/quote/{symbol}'
        self.price = None

    def run(self):
        response = requests.get(self.url)
        if response.status_code == 200: # successful status
            # parse the HTML
            tree = html.fromstring(response.text)
            # get the price in text
            price_text:list = tree.xpath(
                '//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[1]/text()')
            if price_text:
                try:
                    self.price = float(price_text[0].replace(',', ''))
                except ValueError as err:
                    print(err)
                    self.price = None

    def __str__(self):
        return f'{self.symbol}\t{self.price}'