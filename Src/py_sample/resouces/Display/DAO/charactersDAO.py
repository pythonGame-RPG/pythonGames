from DbAccess import *
import DTO.characters as DTO
from settings import *

class CharacterDAO:
    def __init__(self):
        self.ch_name = None


    def execute(self, sql):
        return dbaccess().exe_sql(sql)

    # select文を作成
    def select(self, Dbname):
        # セレクト文を作成
        sql = "Select * from {}".format(Dbname)
        return sql
    
    # 一件登録
    def insert_character(self, characters):
        c_list = []
        c_list = {}
        c_list['name'] = characters.name.get()
        c_list['gene_id'] = characters.gene_id.get()
        c_list['race_id'] = characters.race_id.get()
        c_list['location_id'] = characters.location_id.get()
        c_list['age'] = characters.age.get()
        c_list['birth'] = characters.birth.get()
        c_list['birthplace'] = characters.birthplace.get()
        c_list['title'] = characters.title.get()
        c_list['class1_id'] = characters.class1.get()
        c_list['class2_id'] = characters.class2.get()
        c_list['class3_id'] = characters.class3.get()
        c_list['exp'] = characters.ep.get()
        c_list['level'] = characters.level.get()
        c_list['guild_rank'] = characters.guild_rank.get()
        c_list['guild_point'] = characters.guild_point.get()
        c_list['state'] = characters.state.get()
        c_list['charisma'] = characters.charisma.get()
        c_list['karma'] = characters.karma.get()
        c_list['fortune'] = characters.fortune.get()
        c_list['intelligence'] = characters.intelligence.get()
        c_list['HP'] = characters.HP.get()
        c_list['MP'] = characters.MP.get()
        c_list['sta'] = characters.sta.get()
        c_list['atk'] = characters.atk.get()
        c_list['vit'] = characters.vit.get()
        c_list['mag'] = characters.mag.get()
        c_list['des'] = characters.des.get()
        c_list['agi'] = characters.agi.get()
        c_list['total'] = characters.total.get()
        c_list['talent1_id'] = characters.talent1.get()
        c_list['talent2_id'] = characters.talent2.get()
        c_list['talent3_id'] = characters.talent3.get()
        c_list['is_leader'] = characters.is_leader.get()
        c_list['party1_id'] = characters.party1.get()
        c_list['party2_id'] = characters.party2.get()
        c_list['party3_id'] = characters.party3.get()
        c_list['is_dangeon'] = characters.is_dangeon.get()
        c_list['is_master'] = characters.is_master.get()
        c_list['is_user'] = characters.is_user.get()
        c_list['is_retire'] = characters.is_retire.get()
        c_list['dangeon_id'] = characters.dangeon_id.get()
        c_list['master_id'] = characters.master_id.get()
        c_list['user_id'] = characters.user_id.get()
        c_list['ins_date'] = characters.ins_date
        c_list['ins_id'] = characters.ins_id
        c_list['upd_date'] = characters.upd_date
        c_list['upd_id'] = characters.upd_id

        dbaccess().INSERT_Column(MST_CHARACTERS, c_list)
    

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
