import MetaTrader5 as mt5

def get_tqbr_tickers():
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    all_tickers = mt5.symbols_get()

    tqbr_tickers = [
        ticker_info.name for ticker_info in all_tickers
        if 'TQBR' in ticker_info.path
    ]

    return tqbr_tickers

if __name__ == '__main__':
    print(get_tqbr_tickers())
