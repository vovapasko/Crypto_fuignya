import sqlite3
from UrlBuilder import *
import time


# я не знаю как и где испольовать metadata
# запомни эту мысль и вставь где надо !!!!!!!!!!!!!


class DBHandler:
    __instance = None

    def __init__(self):
        self.db_name = 'crypto.db'
        try:
            # variables, that could be changed for another db
            self.main_table_name = "ALL_ITEMS"
            fields_of_table = """
                id INT PRIMARY KEY     NOT NULL,
                name text              NOT NULL,
                symbol text            NOT NULL,
                website text           NOT NULL,
                time_table_of_currency text
            """

            # connection part
            print("connecting to SQLite")
            self.connection = sqlite3.connect(self.db_name)

            # creating main table and inserting
            self.connection.execute("CREATE table if not exists {} ({});".format(self.main_table_name, fields_of_table))
            self.table_data = self.insert_into_main_table()

        except Exception as e:
            print('Error: connection not established :\n{}'.format(e))
            DBHandler._instance = None  # <--- не уверен что нужно
        else:
            print('Connection established')

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def insert_table_of_currency(self, data, currency_name='example', id_of_currency=0):
        '''
        Insert into table (pam-pam-paaam)
        You can use or id or the name, BUT please transfer one of them into function
        If you enter id and name AND they will be different, program will be oriented on the id
        :param data: data to insert (data['data'] not data['metadata'] or all data )
        :param currency_name: name of currency with spaces if it have
        :param id_of_currency: id of currency in list
        :return:
        '''

        assert id_of_currency != 0 or currency_name != 'example', "Ooooo nooo, I hoped that you will not do it :( " \
                                                                  "\nPlease, insert values into function"

        assert data['id'] == id_of_currency or data['name'] == currency_name, "Error. Insert not correct data"

        if id_of_currency != 0:
            currency_name = data['name']
        elif currency_name != 'example':
            id_of_currency = data['id']
        else:
            raise Exception('this situation is impossible, but like russians says "бережёного бог бережёт" ')

        # variables, that could be changed for another db
        field_name = 'time_table_of_currency'
        values_1, values_2 = '', ''

        # search exists table for insert
        cursor = self.connection.execute(
            "SELECT {} FROM {} where id = {}".format(field_name, self.main_table_name, id_of_currency))
        for row in cursor:
            assert row[0] is not None, "Error, you don't have table for this currency "

        # also, variables that can be changed
        new_currency_name = '_'.join(currency_name.split())
        fields = """rank, last_updated, circulating_supply,
                    total_supply, max_supply, 
                    volume_24h, market_cap, percent_change_1h, price,  
                    percent_change_24h, percent_change_7d, currency_buy"""
        table_name = 'time_table_{}'.format(new_currency_name)

        # value for insert equal to values_1 + values_2
        values_1 = "{}, {}, {}, {}, {}, ".format(data['rank'], data['last_updated'], int(data['circulating_supply']),
                                                 int(data['total_supply']), int(data['max_supply']))

        # value_2 consists of data['quotes']['USD']
        quotes = data['quotes']
        for key in quotes:
            assert key == 'USD', "oh no, i don't know what to do.\ndata : {} \ncurrency : {}".format(data,
                                                                                                     currency_name)
            values_2 = '{}, {}, {}, {}, {}, {}, "{}"'.format(quotes['USD']['volume_24h'], quotes['USD']['market_cap'],
                                                             quotes['USD']['percent_change_1h'], quotes['USD']['price'],
                                                             quotes['USD']['percent_change_24h'],
                                                             quotes['USD']['percent_change_7d'], 'USD')

        # insert values
        self.connection.execute("INSERT into {} ({}) VALUES ({});".format(table_name, fields, values_1 + values_2))
        self.connection.commit()

    def create_new_table_of_currency(self, currency_name='example', id_of_currency=0):
        '''
        Create table (pam-pam-paaam)
        You can use or id or the name, BUT please transfer one of them into function
        If you enter id and name AND they will be different, program will be oriented on the id
        :param currency_name: name of currency with spaces if it have
        :param id_of_currency: id of currency in list
        :return:
        '''

        assert id_of_currency != 0 or currency_name != 'example', "Oooooh nooo, I hoped that you will not do it :( " \
                                                                  "\nPlease, insert values into function"

        if id_of_currency != 0:
            def generator():
                for element in self.table_data:
                    if element['id'] == id_of_currency:
                        yield element['name']
                yield False

            for i in generator():
                assert i, "don't have this id"
                currency_name = i
                break

        new_currency_name = '_'.join(currency_name.split())
        table_name = 'time_table_{}'.format(new_currency_name)
        field_name = 'time_table_of_currency'
        fields_for_table = """
            last_updated   int PRIMARY KEY  NOT NULL,
            rank           int   NOT NULL,
            currency_buy   text  NOT NULL,
            price          int   NOT NULL,
            circulating_supply        int,
            total_supply              int,
            max_supply                int,
            volume_24h               real,
            market_cap               real,
            percent_change_1h        real,
            percent_change_24h       real,
            percent_change_7d        real
        """

        for item in self.table_data:
            # search item in data with same name
            if item['name'] == currency_name:

                cursor = self.connection.execute(
                    "SELECT {} FROM {} where id = {};".format(field_name, self.main_table_name, item['id']))
                for row in cursor:
                    assert row[0] is None, "You already have this table"

                # update main table (change time_table field)
                self.connection.execute(
                    "UPDATE {} set {} = '{}' where id = {};".format(self.main_table_name, field_name, table_name,
                                                                    item['id']))

                # crete table
                self.connection.execute("CREATE TABLE {} ({});".format(table_name, fields_for_table))
                self.connection.commit()
                return

        raise ValueError("Error, don't have this currency")

    def insert_into_main_table(self):

        # get data
        request_data = get_all_data()

        # get old data from table
        select = self.connection.execute("SELECT * FROM {};".format(self.main_table_name))

        # list of id's new data
        new_id = [i['id'] for i in request_data['data']]

        # 4 list fields of select (old data)
        old_id, old_names, old_symbol, old_website = [], [], [], []
        for row in select:
            old_id.append(row[0])
            old_names.append(row[1])
            old_symbol.append(row[2])
            old_website.append(row[3])
            # if old data from table isn't exist in new data from request
            if row[0] not in new_id:
                # deleted query
                self.connection.execute("""DELETE FROM {} where id = {};""".format(self.main_table_name, row[0]))

        # go through new data
        for item in request_data['data']:

            # if we have this id inside table, check that data if correct inside table
            if item['id'] in old_id:
                # update query

                # search index of this record from select query
                index = old_id.index(item['id'])

                # compare old and new info, if they different - update table
                if item['name'] != old_names[index] or item['symbol'] != old_symbol[index] or item['website_slug'] != \
                        old_website[index]:
                    self.connection.execute(
                        """UPDATE {} set name = "{}", symbol = "{}", website = "{}" where id = {};""".format(
                            self.main_table_name, item['name'], item['symbol'], item['website_slug'], item['id']))

                    # ------ only out info
                    old = "{} {} {} {}".format(old_id[index], old_names[index], old_symbol[index], old_website[index])
                    new = "{} {} {} {}".format(item['id'], item['name'], item['symbol'], item['website_slug'])
                    print("old = {} \nnew = {}".format(old, new))  # ------
            # if we don't have this id inside table, insert this new
            else:
                # insert query
                self.connection.execute("""INSERT into {} (id, name, symbol, website)
                values ({}, "{}", "{}", "{}");""".format(self.main_table_name, item['id'], item['name'], item['symbol'],
                                                         item['website_slug']))

        self.connection.commit()
        return request_data['data']


if __name__ == "__main__":
    start = time.time()
    connector = DBHandler()
    connector.create_new_table_of_currency(id_of_currency=10)
    URL3 = get_url_specific_currency(1)
    r3 = requests.get(url=URL3)
    data3 = r3.json()
    connector.insert_table_of_currency('Digitalcoin', data3['data'])
    print(time.time() - start)
