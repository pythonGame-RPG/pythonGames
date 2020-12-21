import numpy as np
from sklearn.preprocessing import MinMaxScaler

def np_unique_with_tolerance(ar, decimals, axis):
    """誤差を許容しつつ，重複を排除した配列を生成する"""
    # 四捨五入する
    ar_rounded = np.round(ar, decimals=decimals)
    # 重複を削除し，代表サンプルのインデックスなどの情報を取得する
    ar_unique, index, inverse, counts = np.unique(ar_rounded, axis=axis, return_index=True, return_inverse=True, return_counts=True)
    return index, inverse, counts

class ThinningManager:
    """間引き処理用クラス"""
    def __init__(self, division_num: int = 100):
        self.X = None  # 間引き後のサンプル全体
        self.index = None  # 代表サンプルのインデックス全体
        self.inverse = None  # 元のサンプルがどの代表サンプルに属するか
        self.counts = None  # 代表サンプルがいくつのサンプルを代表しているか
        self.scaler = MinMaxScaler(feature_range=(0,division_num))

    def fit(self, X: "np.2darray"):
        """間引き処理を実行する"""
        # min max normalizationを実行する
        X_scaled = self.scaler.fit_transform(X)
        # 間引き処理を実行する
        index, inverse, counts = np_unique_with_tolerance(X_scaled, decimals=0, axis=0)
        # 間引き後のデータを登録する
        self.X = X[index]
        self.index = index
        self.inverse = inverse
        self.counts = counts

    def get_X(self):
        """間引き後のデータを取得する"""
        return self.X