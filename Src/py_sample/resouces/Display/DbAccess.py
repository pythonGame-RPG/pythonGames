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
    sql_duplicate = "ON DUPLICATE KEY UPDATE "

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
    
    # sql実行取得
    def upins_sql(self, sql):
        with closing(self.cur) as cursor:
            cursor.execute(sql)
            self.db.commit()
    
    # sql実行Update/Insert
    def exe_sql(self, sql):
        with closing(self.cur) as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
        return rows

    #method
    def DB_activate(self, DBname):
        sql = self.sql_DBactive + DBname
        self.cur.execute(sql)

    
    def INSERT_Column(self, table_name, DTO_data, **duplicate):
        sql = self.sql_insert
        key = ''
        value = ''
        sql = sql + table_name
        sql = sql + " ( "
        for (dkey,dval) in DTO_data.items():
            # valueをセット
            if len(str(dval)) == 0 and len(key) != 0:
                value = value + 'null'
                value = value + " ,"
            else:
                value = value + "'{}'".format(str(dval))
                value = value + " ,"

            # keyをセット
            key = key + str(dkey)
            key = key + " ,"
            
        sql = sql + key[:-1]
        sql = sql + ' ) VALUES ('
        sql = sql + value[:-1]
        sql = sql + ' ) '
        
        # 重複を考慮する場合
        if duplicate != None and len(duplicate) !=0:
            dup = ''
            for dkey,dval in duplicate.items():
                if len(dup) != 0:
                    dup = dup + " , "
                    dup = dup + "{0} = {0} + {1}".format(dkey,dval)
                else:
                    dup = "{0} = {0} + {1}".format(dkey,dval)
            sql = sql + self.sql_duplicate + dup
            
        self.cur.execute(sql)
        self.db.commit()

    # 表示用取得
    def SELECT_All(self, table_name):
        
        sql = "SELECT * from " + table_name
        self.cur.execute(sql)

        return self.cur.fetchall()

    # セレクト文    
    def SELECT_Column(self, table_name,input_column_name,where=None,_in=None):
        for i in range(len(input_column_name)):
            if i == 0:
                column_name = input_column_name[0]
            else:
                column_name = column_name + ',' + input_column_name[i]
        sql = "SELECT " + column_name + " from " + table_name

        # WHERE条件付与
        if where != None:
            where_sql = ''
            for dkey,dval in where.items():
                if len(where_sql) != 0:
                    where_sql = where_sql + ' AND /r/n'
                where_sql = where_sql + dkey + ' = ' + str(dval)
            sql = sql + ' WHERE ' + where_sql

        # IN条件付与
        if _in != None:
            t_in = ''
            if where == None:
                t_in = ' WHERE '
            else:
                t_in = ' AND '
            str_rank = ''
            
            for dkey,dval in _in.items():
                """
                for data in dval:
                    if len(str_rank) != 0:
                        str_rank = str_rank + ', '
                    str_rank = str_rank + data
                t_in = t_in + dkey + ' IN (' + str_rank + ')'
                """
                t_in = t_in + dkey + ' IN ' + str(dval)
            t_in = t_in.replace('[', '(')
            t_in = t_in.replace(']', ')')

            sql = sql + t_in
        
        self.cur.execute(sql)

        return self.cur.fetchall()

    # デストラクタ
    def __del__(self):
        self.db.close()