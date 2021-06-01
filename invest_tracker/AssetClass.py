import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import investpy

# in future versions this class should be inherited by other
# those other will be specific asset class, such as:
#  investment funds
#  real state trust
class Asset:
    

    def __init__(self, code, value, date, name=None):
        """ A class for tracking and analysing investments in a specific
        asset.  

        Args:
            code (str): The code of the investment at the inesting.com website
            value (float): the value of the initial investment in the asset
            date (str): the date that the initial investment was made formated as %d/%m/%Y
            name (str, optional): The name of the asset. Defaults to None.
        """        


        self.code = code
        self.name = name

        today = pd.Timestamp.today().strftime(format="%d/%m/%Y")
        self.historical_values = self.get_historical_values(from_date=date, to_date=today)

        self.transactions = pd.DataFrame(columns=["values", "quantities", "price"],
                                         index=pd.DatetimeIndex([], name="date"))

        self.invest(value=value, invest_date=date)

        
    def get_historical_values(self, from_date, to_date):
        """Function that gets the historical closing value of the asset at investing.com
        through the investpy. 

        Args:
            from_date (str): start date of the series in the format %d/%m/%Y
            to_date (str): ending date of the series in the format %d/%m/%Y

        Returns:
            pd.Series: of the historical values from_date to_date
        """        
        engine = investpy.search_quotes(text=self.code, products=["funds"], countries=["brazil"])
        closings = engine.retrieve_historical_data(from_date=from_date, to_date=to_date)["Close"]
        return closings

    def update_historical_data(self, ref_date=None):
        """Given a referential date, this function updates the historical values through
        the usage of the get_historical_values.
        
        The data will be updated if the referential date is not included into period
        of the already collected historical data. If referential date is not provided
        it will be counted as being today's date.

        If the referential date is before the start date of the historical values,
        the data will be update from the refrential date to one day before the first date
        in our historical values.

        If the refernetial date is after the end date of the historical values,
        the data will be updated from the first date after the last day in the historical values
        to today's date.   


        Args:
            ref_date (str, optional): A referential date. Defaults to None.

        Returns:
           None
        """

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

        start_date = start_date.strftime(format="%d/%m/%Y")
        end_date = end_date.strftime(format="%d/%m/%Y")
        
        additional_data = self.get_historical_values(start_date, end_date)
        self.historical_values =  self.historical_values.append(additional_data).sort_index()


    def withdraw(self, value: float, invest_date=None):
        """Withdraw money from the investment, reducing quantities and values
        own.

        Args:
            value (float): value withdraw
            invest_date (str, optional): date of the withdraw in %d/%m%Y format. Defaults to None.
        """        
        self._update_transactions(value=-value, date=invest_date)
        
    def invest(self, value: float, invest_date=None):
        """Invest money in the investment, increasing quantities and values own.

        Args:
            value (float): value invested
            invest_date (str, optional): date of the investment in %d/%m%Y format. Defaults to None.
        """          
        self._update_transactions(value=value, date=invest_date)


    def _update_transactions(self, value, date):
        """Private function to be used by invest and withdraw
        operationalizing changes in the transaction table.

        Args:
            value (float): [description]
            date (str): [description]
        """        
        timestamp_date = self._format_date(date)
        if timestamp_date not in self.historical_values.index:
            self.update_historical_data(ref_date=timestamp_date)
        
        price = self.historical_values.loc[timestamp_date]
        quantity = value / price
        self.transactions.loc[timestamp_date, ["values", "quantities", "price"]] = [value, quantity, price]


    def get_cummulative_period_roi(self, from_date, to_date=None, period='M'):
        """Get the cummulative ROI from a start period to a end period.
        The cummulative ROI is a series of a accumulated ROI. The cummulative
        ROI is resampled according to a period definition:
          - M: Monthly
          - W: Weekly
          - Y: Yearly

        Args:
            from_date (str): start date in the format %d/%m/%Y
            to_date (str, optional): end date in the format %d/%m/%Y. Defaults to None
            period (str, optional): periodic interval for the resampling of
            the series. Defaults to "M".

        Returns:
            pd.Series: A pandas series with the cummulated ROI over the selected period
        """

        from_timestamp =  self._format_date(from_date)
        to_timestamp =  self._format_date(to_date)

        #selected_historical_values = self.historical_values.loc[from_timestamp:to_timestamp]
        #time_span = selected_historical_values.index

        values_evol = (self.transactions.quantities.
                       reindex(self.historical_values.index).
                       fillna(0).cumsum().
                       mul(self.historical_values).
                       loc[from_timestamp:to_timestamp].
                       resample(period).last())
        
        transactions =  (self.transactions["values"].
                         resample(period).last().
                         reindex(values_evol.index).fillna(0))

        transactions.iloc[0] = values_evol.iloc[0]
        transactions = transactions.cumsum()
        
        return values_evol.div(transactions).sub(1)



    def get_periodic_roi(self, from_date, to_date=None, period='M'):
        """Get the cummulative ROI for a specific periodic definition.
        The periodic definition follows the pandas resample paramter
        configuration. The periodic ROI is resampled according to a
        period definition:
          - M: Monthly
          - W: Weekly
          - Y: Yearly

        Args:
            from_date(str): start date in the format %d/%m/%Y
            to_date (str, optional): end date in the format %d/%m/%Y. Defaults to None
            period (str, optional): periodic interval for the resampling of
            the series. Defaults to "M".

        Returns:
            pd.Series: A pandas series with the periodic ROI
        """

        from_timestamp =  self._format_date(from_date)
        to_timestamp =  self._format_date(to_date)

        #selected_historical_values = self.historical_values.loc[from_timestamp:to_timestamp]
        #time_span = selected_historical_values.index

        df = (self.transactions.reindex(self.historical_values.index).
              fillna(0)[['values', 'quantities']].join(self.historical_values))

        df['quantities'] = df['quantities'].cumsum()
        df['cum_values'] = df['quantities'].mul(df['Close'])
        
        resampled_df = (df.loc[from_timestamp:to_timestamp].
                        resample(period).
                        agg({'values': 'sum', 'cum_values': 'last'}))
                        
        resampled_df['lag_cum_values'] = resampled_df['cum_values'].shift()
        resampled_df = resampled_df.iloc[1:]
        
        return (resampled_df['cum_values'].
                sub(resampled_df['values']).
                div(resampled_df['lag_cum_values']).
                sub(1))

    def plot_roi_evolution(self, from_date, to_date=None, period="M", figsize=(9, 7)):
        """Plot the assets' evolution of cummulative and periodic ROI, from the from_date
        to the to_date.

        Args:
            from_date (str): start date in the format %d/%m/%Y
            to_date (str, optional): end date in the format %d/%m/%Y. Defaults to None
            period (str, optional): periodic interval for the resampling of
            the series. Defaults to "M".
            figsize(tupple (int, int), optional): tupple indicating the figsize
            of the plot. Defaults to (9, 7)
        """

        fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=figsize)
        # https://stackoverflow.com/questions/8248467/matplotlib-tight-layout-doesnt-take-into-account-figure-suptitle
        fig.tight_layout(rect=[0, 0.03, 1, .95])
        
        name = "Asset" if self.name is None else self.name
        fig.suptitle(f'{name} cummulative and periodic ROI')

        # cummulative ROI subplot
        self.get_cummulative_period_roi(from_date, to_date, period).mul(100).plot(ax=ax1)
        ax1.axhline(y=0, linestyle='--', color='grey')
        ax1.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
        ax1.set_ylabel('Cumm. ROI')

        # periodic ROI subplot
        self.get_periodic_roi(from_date, to_date, period).mul(100).plot(ax=ax2)
        ax2.axhline(y=0, linestyle='--', color='grey')
        ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
        ax2.set_ylabel('Period. ROI')

        plt.show()



    @staticmethod
    def _format_date(date_str):
        """Private function used to transform the dates
        into pandas timestamps

        Args:
            date_str (str): date in the format "%d/%m/%Y"

        Returns:
            pd.Timestamp: provided date converted to timestamp
        """        
        if date_str is None:
            return pd.Timestamp.today()
        else:
            date_split = [int(dt) for dt in date_str.split("/")]
            var_list = ["day", "month", "year"]
            date_dict = {var: value for var, value in zip(var_list, date_split)}
            return pd.Timestamp(**date_dict)