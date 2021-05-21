from investments import Investments

asset_X = Investments()
asset_X.invest(value=2000, invest_date="10/01/2005")
asset_X.withdraw(value=100, invest_date="01/01/1999")
asset_X.invest(value=1000)
print(asset_X.cash_flow)
print(asset_X)