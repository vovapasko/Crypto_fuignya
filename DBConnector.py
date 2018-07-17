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

    def create_new_table_of_currency(self, currency_name):
        table_name = 'time_table_{}'.format(currency_name)
        field_name = 'time_table_of_currency'
        fields_for_table = """
        
        """

        for item in self.table_data:
            # search item in data with same name
            if item['name'] == currency_name:

                cursor = self.connection.execute(
                    "select {} from {} where id = {}".format(field_name, self.main_table_name, item['id']))
                for row in cursor:
                    if row[0] is not None:
                        # already have this table
                        return

                # update main table (change time_table field)
                self.connection.execute(
                    "update {} set {} = {} where id = {}".format(self.main_table_name, field_name, table_name,
                                                                 item['id']))

                # crete table
                self.connection.execute("create table {} ({});".format(table_name, fields_for_table))

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
                self.connection.execute("""DELETE FROM {} where id = {}""".format(self.main_table_name, row[0]))

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
    print(time.time() - start)

    # connection = sqlite3.connect("Test")  # print("Connected!")

    # connection.execute('''CREATE TABLE OUR_COMPANY  #          (ID INT PRIMARY KEY     NOT NULL,  #          NAME           TEXT    NOT NULL,  #          AGE            INT     NOT NULL,  #          ADDRESS        CHAR(50),  #          SALARY         REAL);''')

    # print("Table created successfully")  #  # a = 22  # insert = "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \  #       VALUES (123, 'Paul'," + str(a) + ", 'California', 20000.00 )"  # connection.execute(insert)  #  # connection.commit()  #  # connection.close()
