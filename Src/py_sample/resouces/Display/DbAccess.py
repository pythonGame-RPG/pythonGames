# import MySQLdb
import mysql.connector
from contextlib import closing
from select import *

# cl_DB_Manipulate
class dbaccess:
    #Properties
    sql_DBactive = "use "
    sql_cretable = "CREATE TABLE IF NOT EXISTS "
    sql_insert = "INSERT INTO "

    #constructor
    def __init__(self):
        # db
        self.db = mysql.connector.connect(
            user='root',
            passwd='root',
            host='localhost',
            db='dbo'
        )

        # Encoding
        # self.db.set_character_set('utf8')
        self.cur = self.db.cursor(dictionary=True)
        self.cur.execute('SET NAMES utf8;')
        self.cur.execute('SET CHARACTER SET utf8;')
        self.cur.execute('SET character_set_connection=utf8;')
    
    # sql実行
    def exe_sql(self, sql):
        with closing(self.cur) as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
        return rows

    #method
    def DB_activate(self, DBname):
        sql = self.sql_DBactive + DBname
        self.cur.execute(sql)

    def CREATETABLE_City_ID_Name(self, table_name):
        self.table_name = table_name
        sql = self.sql_cretable +\
                self.table_name +\
                " (ID INT," +\
                "City CHAR(100)," +\
                "Country CHAR(100))"
        self.cur.execute(sql)

    def INSERT_City_ID_Name(self, city_data):
        sql = self.sql_insert +\
                self.table_name+\
                " (ID, City, Country) VALUES (%s, %s, %s)"
        self.cur.executemany(sql, city_data)
        self.db.commit()

    def SELECT_Column(self, table_name, *input_column_name):
        for i in range(len(input_column_name)):
            if i == 0:
                column_name = input_column_name[0]
            else:
                column_name = column_name + ',' + input_column_name[i]
        sql = "SELECT " + column_name + " from " + table_name
        self.cur.execute(sql)

        return self.cur.fetchall()

    def __del__(self):
        self.db.close()