import pandas as pd
import matplotlib.pyplot as plt
import investpy

class Asset:
    """Primeira coisa que eu preciso identificar é a de quantidade. 
    """    

    def __init__(self,code, value, date, name=None):
        
        self.code = code
        self.name = name

        today = pd.Timestamp.today().strftime(format="%d/%m/%Y")
        self.historical_values = self.get_historical_values(from_date=date, to_date=today)

        self.transactions = pd.DataFrame(columns=["values", "quantities", "price"],
                                         index=pd.DatetimeIndex([], name="date"))

        self.invest(value=value, invest_date=date)

        
    def get_historical_values(self, from_date, to_date):
        engine = investpy.search_quotes(text=self.code, products=["funds"], countries=["brazil"])
        closings = engine.retrieve_historical_data(from_date=from_date, to_date=to_date)["Close"]
        return closings

    def update_historical_data(self, ref_date=None):
        max_date = self.historical_values.index.max()
        min_date = self.historical_values.index.min()
        today_date = pd.Timestamp.today()
        ref_date = today_date if ref_date is None else ref_date
        
        if ref_date > max_date:
            start_date = max_date + pd.Timedelta(days=1)
            end_date = today_date 
        elif ref_date < min_date:
            end_date = min_date - pd.Timedelta(days=1)
            start_date = ref_date
        else:
            print("Não há necessidade de atualizar os dados")
            return self.historical_values

        start_date = start_date.strftime(format="%d/%m/%Y")
        end_date = end_date.strftime(format="%d/%m/%Y")
        
        additional_data = self.get_historical_values(start_date, end_date)
        self.historical_values =  self.historical_values.append(additional_data).sort_index()


    def withdraw(self, value: float, invest_date=None):
        self._update_transactions(value=-value, date=invest_date)
        
    def invest(self, value: float, invest_date=None):
        self._update_transactions(value=value, date=invest_date)


    def _update_transactions(self, value, date):
        timestamp_date = self._format_date(date)
        if timestamp_date not in self.historical_values.index:
            self.update_historical_data(ref_date=timestamp_date)
        
        price = self.historical_values.loc[timestamp_date]
        quantity = value / price
        self.transactions.loc[timestamp_date, ["values", "quantities", "price"]] = [value, quantity, price]


    def get_comulative_period_roi(self, start, end):
        values_evol = (self.transactions.quantities.
                       reindex(self.historical_values.index).
                       fillna(0).cumsum().
                       mul(self.historical_values).loc[start:end])
        
        transactions =  self.transactions["values"].reindex(values_evol.index).fillna(0)
        transactions.iloc[0] = values_evol.iloc[0]
        transactions = transactions.cumsum()
        
        return values_evol.div(transactions).sub(1)

    def get_periodic_roi(self, period='M'):
        df = (self.transactions.reindex(self.historical_values.index).
              fillna(0)[['values', 'quantities']].join(self.historical_values))
        df['quantities'] = df['quantities'].cumsum()
        df['cum_values'] = df['quantities'].mul(df['Close'])
        
        resampled_df = df.resample(period).agg({'values': 'sum', 'cum_values': 'last'})
        resampled_df['lag_cum_values'] = resampled_df['cum_values'].shift()
        resampled_df = resampled_df.iloc[1:]
        
        return (resampled_df['cum_values'].
                sub(resampled_df['values']).
                div(resampled_df['lag_cum_values']).
                sub(1))

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