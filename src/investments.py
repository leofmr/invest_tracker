import pandas as pd

class Investments:
    def __init__(self):

        self.assets_list = None
        self.assets_regs = None

    
    def import_investments(self, filepath):
        self.assets_regs = pd.read_csv(filepath=filepath)

    