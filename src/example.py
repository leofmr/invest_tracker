from investments import Investments

asset_X = Investments()
asset_X.invest(value=2000, invest_date="10/01/2005")
asset_X.withdraw(value=100, invest_date="01/01/1999")
asset_X.invest(value=1000)

values_list = [("09/01/2004", 200), ("11/01/2005", 2500), ("01/01/2006", 2900), ("21/05/2021", 6200)]
for date_str, current_value in values_list:
    asset_X.update_value(value=current_value, measure_date=date_str)

print(asset_X.cash_flow)
print(asset_X)
print(asset_X.roi(start_date="01/01/2005", end_date="21/05/2021"))