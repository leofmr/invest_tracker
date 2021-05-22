import pandas as pd
from datetime import date, datetime, timedelta

class Investments:
    """Primeira coisa que eu preciso identificar é a de quantidade. 
    """    

    def __init__(self):
        
        index = pd.DatetimeIndex([], name="date")
        self.cash_flow = pd.Series(data=[], index=index , dtype="float64", name="cash_flow")

        self.current_values = pd.Series(data=[], index=index, dtype="float64", name="current_values")
    
    def withdraw(self, value: float, invest_date=None):
        timestamp_date = self._format_date(invest_date)
        self.cash_flow.loc[timestamp_date] = -value
        
    def invest(self, value: float, invest_date=None):
        timestamp_date = self._format_date(invest_date)
        self.cash_flow.loc[timestamp_date] = value

    def update_value(self, value, measure_date=None):
        timestamp_date = self._format_date(measure_date)
        self.current_values.loc[timestamp_date] = value
    

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
        

        start_date = (self.cash_flow.index.min() if start_date is None
                      else self._format_date(start_date))
        
        end_date = (self.current_values.index.max() if end_date is None
                    else self._format_date(end_date))

        value_series = self.current_values.loc[start_date:end_date]
        
        start_date += pd.Timedelta(days=1)
        flow_series = self.cash_flow.loc[start_date:end_date]
        
        starting_balance = value_series.first("1D").iloc[0]
        ending_balance = value_series.last("1D") .iloc[0]
        net_balance = flow_series.sum()

        return ((ending_balance - net_balance) / starting_balance) - 1

    @staticmethod
    def _format_date(date_str):
        if date_str is None:
            return pd.Timestamp.today()
        else:
            date_split = [int(dt) for dt in date_str.split("/")]
            var_list = ["day", "month", "year"]
            date_dict = {var: value for var, value in zip(var_list, date_split)}
            return pd.Timestamp(**date_dict)

    def __repr__(self) -> str:
        net_invest = self.cash_flow.sum()
        initial_date = self.cash_flow.index.min().strftime('%d-%m-%Y')
        accumulated_roi = self.roi()
        last_reg = self.current_values.last("1D")
        last_value = last_reg.iloc[0]
        last_date = last_reg.index[0].strftime('%d-%m-%Y')

        net_investment_str = f"Net investment of R${net_invest:,.2f}"
        most_recent_value_str = f"With a current value of R${last_value:,.2f} in {last_date}"
        accumulated_roi_str = f"And a accumulated ROI of {accumulated_roi:.2%} since {initial_date}"
        repr_list = [net_investment_str, most_recent_value_str, accumulated_roi_str]

        return "\n".join(repr_list) 