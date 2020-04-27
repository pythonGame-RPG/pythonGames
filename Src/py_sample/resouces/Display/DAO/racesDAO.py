from DbAccess import *
import DTO.races as DTO

class RaceDAO:

    def __init__(self):
        self.race_name = [""]  

    def execute(self, sql):
        return dbaccess().exe_sql(sql)

    # select文を作成
    def select(self, Dbname):
        # セレクト文を作成
        sql = "Select * from {}".format(Dbname)
        return sql
    
    # gene_nameをセット
    def set_gene_name(self):
        self.data = {'gene_id':self.gene_id, 'gene_name':self.gene_name}
        gene_name = [""]
        # geneデータ取得
        genes = self.select_gene()
        for data in genes:
            gene_name.append(data)
        
        return gene_name

    def where(self, select, datas, bigger = None, smaller = None):
        where_list = []
        # keyとvalueをイコール関係で結びつける
        try:
            for dkey, dvalue in datas.items():
                where_list.append(dkey + ' = '  + '"{}"'.format(dvalue))
        except AttributeError:
            pass
        try:
            # 大なり
            for dkey, dvalue in bigger.items():
                where_list.append(dkey + ' >= '  + '"{}"'.format(dvalue))
        except AttributeError:
            pass
        try:
            # 小なり
            for dkey, dvalue in bigger.items():
                where_list.append(dkey + ' <= '  + '"{}"'.format(dvalue))
        except AttributeError:
            pass
        
        # AND区切りの文字列に変換
        where = " AND ".join(map(str, where_list))
        where = " where " + where
        return select + where
