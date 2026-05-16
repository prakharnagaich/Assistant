from nsepython import nse_live_index

# Fetch live Nifty 50 data
nifty_data = nse_live_index("NIFTY 50")

# Extract current price
print(f"Nifty 50 Current Price: {nifty_data['lastPrice']}")