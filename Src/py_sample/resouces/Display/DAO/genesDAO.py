import tkinter as tk
from DbAccess import *
from DTO.genes import *
from settings import *

class GeneDAO:
    def __init__(self):
        self.gene_name = [""]  
    
    def execute(self, sql):
        return dbaccess().exe_sql(sql)

    # select文を作成
    def select_gene(self, where = None):
        return dbaccess().SELECT_All(MST_GENES)
    
    # gene_nameをセット
    def set_gene(self):
        genes = self.select_gene()
        for key, val in genes.items():
            data = {'gene_id':genes.gene_id, 'gene_name':genes.gene_name, 'gene_rank':genes.gene_rank}
            self.gene_name.append(data)

        # geneデータ取得
        return self.gene_name

    # def select
