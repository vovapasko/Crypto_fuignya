import sqlite3
from UrlBuilder import *


class DBHandler:
    __instance = None

    def __init__(self):
        self.db_name = 'crypto.db'
        try:
            # variables, that could be changed for another db
            main_table_name = "ALL_ITEMS"
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
            self.connection.execute("CREATE table if not exists {} ({});".format(main_table_name, fields_of_table))
            self.insert_into_main_table()

        except e:
            print('Error: connection not established :\n{}'.format(e))
            DBHandler._instance = None  # <--- не уверен что нужно
        else:
            print('Connection established')

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def insert_into_main_table(self):
        # variables, that could be changed for another db
        main_table_name = "ALL_ITEMS"

        # get data
        data1 = get_all_data()

        # get old data from table
        select = self.connection.execute("SELECT * FROM {};".format(main_table_name))

        # list of id's new data
        new_id = [i['id'] for i in data1['data']]

        # 4 list fields of select (old data)
        created_id, created_names, created_symbol, created_website = [], [], [], []
        for row in select:
            created_id.append(row[0])
            created_names.append(row[1])
            created_symbol.append(row[2])
            created_website.append(row[3])
            # if old data from table isn't exist in new data from request
            if row[0] not in new_id:
                # deleted query
                self.connection.execute("""DELETE FROM {} where id = {}""".format(main_table_name, row[0]))

        # go through new data
        for item in data1['data']:

            # if we have this id inside table, check that data if correct inside table
            if item['id'] in created_id:
                # update query
                index = created_id.index(item['id'])

                if item['name'] != created_names[index] or item['symbol'] != created_symbol[index] or \
                        item['website_slug'] != created_website[index]:
                    self.connection.execute(
                        """UPDATE {} set name = "{}", symbol = "{}", website = "{}" where id = {};""".format(
                            main_table_name, item['name'], item['symbol'], item['website_slug'], item['id']))

                    # ------ only out info
                    old = "{} {} {} {}".format(created_id[index], created_names[index], created_symbol[index],
                                               created_website[index])
                    new = "{} {} {} {}".format(item['id'], item['name'], item['symbol'], item['website_slug'])
                    print("old = {} \nnew = {}".format(old, new))
                    # ------
            # if we don't have this id inside table, inset this new
            else:
                # insert query
                self.connection.execute("""INSERT into {} (id, name, symbol, website)
                values ({}, "{}", "{}", "{}");""".format(main_table_name, item['id'], item['name'], item['symbol'],
                                                         item['website_slug']))

        self.connection.commit()


if __name__ == "__main__":

    connector = DBHandler()

    # connection = sqlite3.connect("Test")
    # print("Connected!")

    # connection.execute('''CREATE TABLE OUR_COMPANY
    #          (ID INT PRIMARY KEY     NOT NULL,
    #          NAME           TEXT    NOT NULL,
    #          AGE            INT     NOT NULL,
    #          ADDRESS        CHAR(50),
    #          SALARY         REAL);''')

    # print("Table created successfully")
    #
    # a = 22
    # insert = "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
    #       VALUES (123, 'Paul'," + str(a) + ", 'California', 20000.00 )"
    # connection.execute(insert)
    #
    # connection.commit()
    #
    # connection.close()
