import pandas as pd
from datetime import date, datetime

class Investments:
    """Primeira coisa que eu preciso identificar é a de quantidade. 
    """    
    
    def __init__(self):
        self.cash_flow = pd.DataFrame(columns=["date", "value"])
        self.current_values = pd.DataFrame(columns=["date", "value"])

    
    def withdraw(self, value: float, invest_date=None):
        self._insert_cash_flow_change(invest_date, value, False)
        

    def invest(self, value: float, invest_date=None):
        self._insert_cash_flow_change(invest_date, value, True)


    def _insert_cash_flow_change(self, invest_date, value, is_positive):
        value = value if is_positive else -value
        if invest_date is None:
            date_obj = date.today()
        else: 
            date_obj = datetime.strptime(invest_date, "%d/%m/%Y").date()
        reg = pd.Series({"date": date_obj, "value": value})
        
        self.cash_flow = self.cash_flow.append(reg, ignore_index=True)