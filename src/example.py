from investments import Investments

asset = Investments()

value_list = [7585.63, 10389.38, 10476.59, 10683.55,
              10594.26, 10504.96, 9685.36, 9679.61, 9679.61,
              9679.61, 9679.61, 9673.85, 10015.93, 10072.99, 9866.50,
              9891.93, 10145.41, 10145.41]

dates_list = ["17/01/2021",	"24/01/2021", "31/01/2021",	"07/02/2021", "14/02/2021",
	          "21/02/2021", "28/02/2021", "07/03/2021", "14/03/2021", "21/03/2021",
              "28/03/2021",	"04/04/2021", "11/04/2021",	"18/04/2021", "25/04/2021",
              "02/05/2021", "09/05/2021", "16/05/2021"]

asset.invest(value=value_list[0], invest_date=dates_list[0])
for date_str, value in zip(dates_list, value_list):
    asset.update_value(value, date_str)

print(asset.roi())