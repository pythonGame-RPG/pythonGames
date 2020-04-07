# initialize pygame and create window
import re

# Game Loop
class validate:
    def __init__(self):
        self.digitReg = re.compile(r'^[0-9]+$')
    # 半角英数字判定
    def isdigit(self,s):
        return self.digitReg.match(s) is not None

    # 文字列長さ判定
    def v_length(self, s, limnum):
        return len(s) <= limnum