import tkinter as tk
from DbAccess import *
from DTO.genes import *
from settings import *

class GeneDAO():
    def __init__(self):
        self.gene_name = [""] 
        self.gene_list = {}
        self.gene_cbo = []
    
    def execute(self, sql):
        return dbaccess().exe_sql(sql)

    # select文を作成
    def select_gene(self):
        _comb = ('gene_id', 'g_rank', 'gene_name')
        return dbaccess().SELECT_Column(MST_GENES,'gene_id', 'gene_name', 'g_rank')
    
    # gene_nameをセット
    def set_gene(self):
        genes = self.select_gene()
        for gene in genes:
            # コンボボックスのリストに追加
            self.gene_list[gene['gene_id']] = gene['g_rank'] + ':' + gene['gene_name']
            # self.gene_cbo.append(gene['gene_name'])

        # geneデータ
        return self.gene_list

    # def select
