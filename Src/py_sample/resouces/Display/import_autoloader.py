from importlib import import_module
import os
"""
オートローダー
@param basepath
@return class
"""
class im:
    def auto_load(self, basepath):
        #basepath = os. 
        """
         TODO:
         ①basepathからドキュメントルートを左から切り取り
         ②basepathの/を.に変換
        """
        modele = import_module(basepath)
        return module
