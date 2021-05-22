import pandas as pd
from datetime import date, datetime

class Investments:
    """Primeira coisa que eu preciso identificar é a de quantidade. 
    """    
    date_format = "%d/%m/%Y"

    def __init__(self):
        
        self.cash_flow = pd.DataFrame({"date": pd.Series([], dtype="datetime64[ns]"),
                                       "value": pd.Series([], dtype="float")})
                                       
        self.current_values = pd.DataFrame({"date": pd.Series([], dtype="datetime64[ns]"),
                                            "value": pd.Series([], dtype="float")})

    
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

    def roi(self, start_date=None, end_date=None):
        """For a selected period, compute the ROI of the investment (corrected for cash flows)
        Following this reference:
            - https://www.fool.com/about/how-to-calculate-investment-returns/
    
        Args:
            start_date (str, optional): Start date of the period. Defaults to None.
            end_date (str, optional): End date of the period. Defaults to None.

        Returns:
            float: The Return on Investment for the selected period
        """
        if start_date is None:
            start_date = self.cash_flow["date"].min()
        else:        
            start_date = datetime.strptime(start_date, self.date_format).date()
        
        if end_date is None:
            end_date = self.current_values["date"].max()
        else:
            end_date = datetime.strptime(end_date, self.date_format).date()
        
        values_series = self.current_values.groupby("date")['value'].mean().loc[start_date:end_date].sort_index()
        flows_series = self.cash_flow.groupby("date")["value"].sum().loc[start_date:end_date].sort_index()
        
        starting_balance = values_series.iloc[0]
        ending_balance = values_series.iloc[-1] 
        net_balance = flows_series.sum()

        return ((ending_balance - net_balance) / starting_balance) - 1




    
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