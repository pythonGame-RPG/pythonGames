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
    sql_update = "UPDATE {} SET "

    #constructor
    def __init__(self):
        # db
        self.db = mysql.connector.connect(
            user='root',
            passwd='root',
            host='localhost',
            db='dbo'
            #,local_infile=True
        )
        # Encoding
        # self.db.set_character_set('utf8')
        self.cur = self.db.cursor(dictionary=True)
        self.cur.execute('SET NAMES utf8;')
        self.cur.execute('SET CHARACTER SET utf8;')
        self.cur.execute('SET character_set_connection=utf8;')
        self.res = False
    
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

    # 登録処理
    # param = テーブル名、DTO、重複ディクショナリ
    def INSERT_Column(self, table_name, DTO_data, **duplicate):
        sql = self.sql_insert
        key = ''
        value = ''
        sql = sql + table_name
        sql = sql + " ( "
        for (dkey,dval) in DTO_data.items():
            # valueをカンマ区切りのstrで取得
            if len(str(dval)) == 0 and len(key) != 0:
                value = value + 'null'
                value = value + " ,"
            else:
                value = value + "'{}'".format(str(dval))
                value = value + " ,"

            # keyをカンマ区切りのstrで取得
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
        if self.cur.lastrowid != 0:
            return self.cur.lastrowid
        else:
            return self.cur.rowcount

    # バルクイン処理
    # param = テーブル名、DTO、重複ディクショナリ
    def BULK_INSERT_Column2(self, table_name, values, num):

        str_s = ''
        for i in range(num):
            str_s = str_s + '%s,'
        str_s = str_s[:-1]

        # TODO:deliminatorとかの設定
        print("Insert bulk {}".format(table_name))
        insert_sql = "INSERT INTO {0} values ({1})".format(table_name,str_s)

        self.cur.executemany(insert_sql, values)
        self.db.commit()

    # バルクイン処理（ローカルファイル経由）最速
    # param = テーブル名、DTO、重複ディクショナリ
    def BULK_INSERT_Column(self, table_name, csv_path):

        # TODO:deliminatorとかの設定
        sql = """
            SET GLOBAL local_infile=on;
            LOAD DATA LOCAL INFILE '{0}'
            INTO TABLE  {1} FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' 
            LINES TERMINATED BY '\n' 
            """.format(csv_path, table_name)
        
        self.cur.execute(sql, multi=True)
        self.db.commit()

    # 更新処理
    # param = テーブル名、DTO、抽出条件ディクショナリ、non_strフラグ
    def UPDATE_Column(self, table_name, DTO_data, where, nonStr=False):
        sql = self.sql_update.format(table_name)
        dataList = []
        # 更新項目を編集
        for (dkey,dval) in DTO_data.items():
            # 更新項目をリストで取得
            if len(str(dval)) == 0:
                dataList.append(dkey + ' = null')
            else:
                if nonStr:
                    dataList.append(dkey + ' = ' + str(dval))
                else:
                    dataList.append(dkey + ' = ' + '\"' +  str(dval) + '\"')
        
        data_str = " ,".join(dataList)
        sql = sql + data_str

        # where条件を編集
        if where != None and len(where) !=0:
            
            dataList = []

            # 更新項目を編集
            for (dkey,dval) in where.items():
                # 更新項目をリストで取得
                # nullの場合IS NULL表記
                if str(dval) == 'null':
                    dataList.append(dkey + ' IS null')
                else:
                    if len(str(dval)) == 0:
                        dataList.append(dkey + ' = null')
                    else:
                        if nonStr:
                            dataList.append(dkey + ' = ' + str(dval))
                        else:
                            dataList.append(dkey + ' = ' + '\"' +  str(dval) + '\"')
            
            data_str = " AND ".join(dataList)
            sql = sql + ' where ' + data_str
            
        self.cur.execute(sql)
        self.db.commit()
        return self.cur.rowcount

    # 表示用取得
    def SELECT_All(self, table_name):
        
        sql = "SELECT * from " + table_name
        self.cur.execute(sql)

        return self.cur.fetchall()

    # セレクト文
    def SELECT_Column_A(self,table_name,columns, where=None, sort=None):
        for i in range(len(columns)):
            if i == 0:
                column_name = columns[0]
            else:
                column_name = column_name + ',' + columns[i]
        sql = "SELECT " + column_name + " from " + table_name

        if where != None:
            sql = sql +  ' where ' + where
            
        if sort != None:
            sql = sql +  ' order by ' + sort

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
                    where_sql = where_sql + ' AND \r\n'
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
        
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except:
            self.db.rollback()
            return self.res
    
    def DELETE_Column(self, table_name, where):

        sql = "DELETE FROM {}".format(table_name)

        where_sql = ''
        for dkey,dval in where.items():
            if len(where_sql) != 0:
                where_sql = where_sql + ' AND '
            where_sql = where_sql + dkey + ' = ' + str(dval)
        sql = sql + ' WHERE ' + where_sql

        try:
            self.cur.execute(sql)
            return self.db.commit()
        except:
            self.db.rollback()
            return self.res

    def BASIC_DELETE(self, table_name, where):

        sql = "DELETE FROM {0} {1}".format(table_name, where)

        try:
            self.cur.execute(sql)
            return self.db.commit()
        except:
            self.db.rollback()
            return self.res

    # デストラクタ
    def __del__(self):
        self.db.close()