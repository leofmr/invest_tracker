import pandas as pd
from datetime import date, datetime

class Investments:
    """Primeira coisa que eu preciso identificar é a de quantidade. 
    """    
    
    def __init__(self):
        self.cash_flow = pd.DataFrame(columns=["date", "value"])
        self.current_values = pd.DataFrame(columns=["date", "value"])

    
    def withdraw(self, value: float, invest_date=None):
        self._insert_cash_flow_change(invest_date=invest_date, value=value, is_positive=False)
        

    def invest(self, value: float, invest_date=None):
        self._insert_cash_flow_change(invest_date=invest_date, value=value, is_positive=True)


    def _insert_cash_flow_change(self, invest_date, value, is_positive):
        reg = self._format_reg(reg_date=invest_date, value=value, is_positive=is_positive)
        self.cash_flow = self.cash_flow.append(reg, ignore_index=True)

    def update_value(self, value, measure_date=None):
        reg = self._format_reg(reg_date=measure_date, value=value, is_positive=True)
        self.current_values = self.current_values.append(reg, ignore_index=True)
    
    @staticmethod
    def _format_reg(reg_date, value, is_positive):
        value = value if is_positive else -value
        if reg_date is None:
            date_obj = date.today()
        else: 
            date_obj = datetime.strptime(reg_date, "%d/%m/%Y").date()
        return pd.Series({"date": date_obj, "value": value})

    def __repr__(self) -> str:
        total_invest = self.cash_flow['value'].sum()
        return f'Total investment: {total_invest}'