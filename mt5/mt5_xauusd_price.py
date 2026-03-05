import MetaTrader5 as mt5
from datetime import datetime

# Initialize connection to MT5
if not mt5.initialize():
    print("Initialize() failed")
    print("Error code:", mt5.last_error())
    quit()

print("Connected to MT5")

symbol = "XAUUSD"

# Ensure symbol is available
if not mt5.symbol_select(symbol, True):
    print(f"Failed to select {symbol}")
    mt5.shutdown()
    quit()

# Get latest tick data
tick = mt5.symbol_info_tick(symbol)

if tick is None:
    print("Failed to get tick data")
else:
    print("Time:", datetime.fromtimestamp(tick.time))
    print("Bid:", tick.bid)
    print("Ask:", tick.ask)
    print("Spread:", round(tick.ask - tick.bid, 4))

# Shutdown connection
mt5.shutdown()