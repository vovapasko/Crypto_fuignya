import requests

base_url = "https://api.coinmarketcap.com/v2/"
listings = "listings/"
ticker = "ticker/"


# class UrlAllCurrencyBuilder():
#     @staticmethod
#     def get_url():
#         return base_url + listings

def get_url_all_currency():
    return base_url + listings


def get_all_data():
    url = get_url_all_currency()
    r1 = requests.get(url=url)
    return r1.json()


#
# class UrlTickerBuilder():
#     @staticmethod
#     def get_url():
#         return base_url + ticker
#
#     @staticmethod
#     def get_url(limit, start=1, sort="rank", structure="dictionary", convert="USD"):
#         return base_url + ticker + "?limit=" + str(limit) + "&start=" + str(start) \
#                + "&sort=" + sort + "&structure=" + structure + "&convert=" + convert


def get_url_ticker():
    return base_url + ticker


def get_url_ticker(limit, start=1, sort="rank", structure="dictionary", convert="USD"):
    return base_url + ticker + "?limit=" + str(limit) + "&start=" + str(
        start) + "&sort=" + sort + "&structure=" + structure + "&convert=" + convert


# class UrlSpecificCurrencyBuilder():
#     @staticmethod
#     def get_url(id, convert="USD"):
#         print(base_url + ticker + str(id) + "/?convert=" + convert)
#         return base_url + ticker + str(id) + "/?convert=" + convert

def get_url_specific_currency(id, convert="USD"):
    return base_url + ticker + str(id) + "/?convert=" + convert
