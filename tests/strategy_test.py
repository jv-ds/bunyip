from data_load import get_underlying_stock_list, get_5d_sma_list, get_30d_sma_list

start_date = "2026-01-01"
end_date = "2026-08-24"   


thirty_d = get_30d_sma_list(start_date, end_date)
five_d = get_5d_sma_list(start_date, end_date)
underlying_close, date, raw_dict = get_underlying_stock_list(start_date, end_date)

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(date, underlying_close, label="Underlying Close", color="black")
plt.plot(date, five_d, label="5-Day SMA", color="dodgerblue")
plt.plot(date, thirty_d, label="30-Day SMA", color="crimson")

plt.xlabel("Date")
plt.ylabel("Price")
plt.title("Underlying vs SMAs")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()