#!/usr/bin/env python
#------------------------------------------------------------------------------------------------#
# Gemini Public Trades — Last 25 BTC/USD trades (no auth required)
#------------------------------------------------------------------------------------------------#

import requests
from datetime import datetime, timezone
from prettytable import PrettyTable
import pytz

LA_TZ = pytz.timezone('America/Los_Angeles')
BASE_URL = "https://api.gemini.com"

GREEN = '\033[92m'
RED   = '\033[91m'
RESET = '\033[0m'

#------------------------------------------------------------------------------------------------#
def main():
    response = requests.get(f"{BASE_URL}/v1/trades/btcusd", params={"limit_trades": 25})
    response.raise_for_status()
    trades = response.json()

    # Sort oldest first (latest at bottom)
    trades.sort(key=lambda t: t['timestamp'])

    table = PrettyTable()
    table.field_names = ["#", "Trade ID", "Date/Time (LA)", "Type", "BTC Amount", "Price", "Total Value"]
    table.align["#"]           = "r" 
    table.align["Trade ID"]    = "l" 
    table.align["Date/Time (LA)"] = "l" 
    table.align["Type"]        = "c" 
    table.align["BTC Amount"]  = "r" 
    table.align["Price"]       = "r" 
    table.align["Total Value"] = "r" 

    for idx, trade in enumerate(trades, 1): 
        ts = datetime.fromtimestamp(trade['timestamp'], tz=timezone.utc).astimezone(LA_TZ)
        amount = float(trade['amount'])
        price  = float(trade['price'])
        total  = amount * price
        side   = trade['type'].lower()
        tid    = trade['tid']

        if side == 'buy':
            c = GREEN
            label = '[BUY]'
        else:
            c = RED 
            label = '[SELL]'

        table.add_row([
            f"{c}{idx}{RESET}",
            f"{c}{tid}{RESET}",
            f"{c}{ts.strftime('%Y-%m-%d %H:%M:%S')}{RESET}",
            f"{c}{label}{RESET}",
            f"{c}{amount:.5f}{RESET}",
            f"{c}${price:,.2f}{RESET}",
            f"{c}${total:,.4f}{RESET}",
        ])  

    print(f"\n  Last 25 Public BTC/USD Trades on Gemini\n")
    print(table)
    print()

#------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    main()
