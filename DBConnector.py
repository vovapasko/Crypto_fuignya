import sqlite3

connection = sqlite3.connect("Test")
print("Connected!")

# connection.execute('''CREATE TABLE COMPANY
#          (ID INT PRIMARY KEY     NOT NULL,
#          NAME           TEXT    NOT NULL,
#          AGE            INT     NOT NULL,
#          ADDRESS        CHAR(50),
#          SALARY         REAL);''')


print("Table created successfully")

a = 22
insert = "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (123, 'Paul'," + str(a) + ", 'California', 20000.00 )"
connection.execute(insert)

connection.commit()

connection.close()
