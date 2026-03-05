import MetaTrader5 as mt5
import time

# --- SETTINGS ---
SYMBOL = "XAUUSD"
LOT = 0.01  # small for demo safety
SL_PIPS = 45
TP_PIPS = 100

# --- CONNECT ---
if not mt5.initialize():
    print("Initialize failed:", mt5.last_error())
    quit()

print("Connected to MT5")

# --- SYMBOL CHECK ---
symbol_info = mt5.symbol_info(SYMBOL)
if symbol_info is None:
    print("Symbol not found")
    mt5.shutdown()
    quit()

if not symbol_info.visible:
    mt5.symbol_select(SYMBOL, True)

point = symbol_info.point
pip_value = point * 10  # Gold pip conversion

tick = mt5.symbol_info_tick(SYMBOL)
price = tick.ask

sl = price - SL_PIPS * pip_value
tp = price + TP_PIPS * pip_value

# --- SEND BUY ORDER ---
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": SYMBOL,
    "volume": LOT,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "sl": sl,
    "tp": tp,
    "deviation": 20,
    "magic": 1001,
    "comment": "Python test trade",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
}

result = mt5.order_send(request)

if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("Order failed, retcode:", result.retcode)
    print("Error:", mt5.last_error())
    mt5.shutdown()
    quit()

print("BUY order placed successfully")
mt5.shutdown()
quit()

time.sleep(2)

# --- GET OPEN POSITION ---
positions = mt5.positions_get(symbol=SYMBOL)

if positions:
    position = positions[0]
    print("Open position ticket:", position.ticket)
else:
    print("No open positions found")
    mt5.shutdown()
    quit()

# --- CLOSE POSITION ---
close_request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": SYMBOL,
    "volume": position.volume,
    "type": mt5.ORDER_TYPE_SELL,
    "position": position.ticket,
    "price": mt5.symbol_info_tick(SYMBOL).bid,
    "deviation": 20,
    "magic": 1001,
    "comment": "Closing trade",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
}

close_result = mt5.order_send(close_request)

if close_result.retcode != mt5.TRADE_RETCODE_DONE:
    print("Close failed, retcode:", close_result.retcode)
    print("Error:", mt5.last_error())
else:
    print("Position closed successfully")

mt5.shutdown()
print("Done.")