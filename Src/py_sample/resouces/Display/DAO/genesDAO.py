import tkinter as tk
from DbAccess import *
from DTO.genes import *
from settings import *

class GeneDAO():
    def __init__(self):
        self.gene_list = {}
        self.gene_cbo = [""]
        self.genes = None
    
    def execute(self, sql):
        return dbaccess().exe_sql(sql)

    # select文を作成
    def select_gene(self):
        return dbaccess().SELECT_Column(MST_GENES, '*', ' concat(g_rank, ":", gene_name) as gene_cbo')
    
    # gene_nameをセット
    def set_gene(self):
        self.genes = self.select_gene()
        for gene in self.genes:
            # コンボボックスのリストに追加
            # self.gene_list[gene['gene_id']] = gene['g_rank'] + ':' + gene['gene_name']
            self.gene_cbo.append(gene['gene_cbo'])
        # self.gene_cbo.append("")

        # geneデータ
        return self.gene_cbo

    # レベル異存なし取得
    def pickup_gene(self, gene_cbo):
        s_gene = [gene for gene in self.genes if gene['gene_cbo'] == gene_cbo]
        return s_gene[0]

    # 一件登録
    def insert_gene(self, genes):
        g_list = {}
        g_list['gene_name'] = genes.gene_name.get()
        g_list['is_gene_name'] = genes.is_gene_name.get()
        g_list['personal_code'] = genes.personal_code.get()
        g_list['s_HP'] = genes.s_HP.get()
        g_list['s_MP'] = genes.s_MP.get()
        g_list['s_sta'] = genes.s_sta.get()
        g_list['s_atk'] = genes.s_atk.get()
        g_list['s_vit'] = genes.s_vit.get()
        g_list['s_mag'] = genes.s_mag.get()
        g_list['s_des'] = genes.s_des.get()
        g_list['s_agi'] = genes.s_agi.get()
        g_list['total_sense'] = genes.total_sense.get()
        g_list['g_rank'] = genes.g_rank.get()
        g_list['ins_date'] = genes.ins_date
        g_list['ins_id'] = genes.ins_id.get()
        g_list['upd_date'] = genes.upd_date
        g_list['upd_id'] = genes.upd_id.get()

        dbaccess().INSERT_Column(MST_GENES, g_list)


