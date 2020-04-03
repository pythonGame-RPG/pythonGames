# initialize pygame and create window
import re

# Game Loop
class validate:
    digitReg = re.compile(r'^[0-9]+$')
    # 半角英数字判定
    def isdigit(self,s):
        return digitReg.match(s) is not None

    # 文字列長さ判定
    def v_length(self, s, limnum):
        return s.length<=limnum