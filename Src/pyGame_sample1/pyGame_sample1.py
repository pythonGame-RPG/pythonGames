from pygame.locals import *
from random import randint
import pygame
import time
import Characters
import App
import Game
import Player
# MySQLdbのインポート
import MySQLdb
 
# データベースへの接続とカーソルの生成
connection = MySQLdb.connect (
    host='localhost',
    user='root',
    passwd='root',
    db='dbo'
    )
cursor = connection.cursor()
 
# ここに実行したいコードを入力します
cursor.execute("SELECT * FROM characters");
 
# 保存を実行
connection.commit()
 
# 接続を閉じる
connection.close()

if __name__ == "__main__" :
    theApp = App.App()
    theApp.on_execute()
