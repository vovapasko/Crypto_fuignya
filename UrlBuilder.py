base_url = "https://api.coinmarketcap.com/v2/"
listings = "listings/"
ticker = "ticker/"

# class UrlAllCurrencyBuilder():
#     @staticmethod
#     def get_url():
#         return base_url + listings

def getUrlAllCurrency():
    return base_url + listings


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


def getUrlTicker():
    return base_url + ticker


def getUrlTicker(limit, start=1, sort="rank", structure="dictionary", convert="USD"):
    return base_url + ticker + "?limit=" + str(limit) + "&start=" + str(start) \
           + "&sort=" + sort + "&structure=" + structure + "&convert=" + convert


# class UrlSpecificCurrencyBuilder():
#     @staticmethod
#     def get_url(id, convert="USD"):
#         print(base_url + ticker + str(id) + "/?convert=" + convert)
#         return base_url + ticker + str(id) + "/?convert=" + convert

def getUrlSpecificCurrency(id, convert="USD"):
    return base_url + ticker + str(id) + "/?convert=" + convert
