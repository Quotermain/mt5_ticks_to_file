from utils.get_tqbr_tickers import get_tqbr_tickers
from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
import pickle
from sys import argv

if argv[1] == 'problem_tickers':
    with open('problem_tickers.pickle', 'rb') as file:
        ALL_TICKERS = pickle.load(file)
elif argv[1] == 'all_tickers':
    ALL_TICKERS = get_tqbr_tickers()

problem_tickers = []
def run(ticker):
    """
    Establishes connection with the terminal, parses prices,
    as is, shuts down the connection
    """
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    utc_from = datetime(2020, 12, 1)
    utc_to = datetime(2021, 4, 23)
    ticks = mt5.copy_ticks_range(ticker, utc_from, utc_to, mt5.COPY_TICKS_TRADE)
    mt5.shutdown()

    ticks_frame = pd.DataFrame(ticks)
    ticks_frame['datetime']=pd.to_datetime(ticks_frame['time'], unit='s')
    ticks_frame['date'] = [d.date() for d in ticks_frame['datetime']]
    ticks_frame['time'] = [d.time() for d in ticks_frame['datetime']]

    ticks_frame = ticks_frame.loc[:, ['datetime', 'date', 'time', 'last']]
    ticks_frame.to_csv(f'data/{ticker}.csv', index=False)

if __name__ == '__main__':
    for ticker in ALL_TICKERS:
        try:
            run(ticker)
        except Exception as e:
            problem_tickers.append(ticker)
            continue
    with open('problem_tickers.pickle', 'wb') as file:
        pickle.dump(problem_tickers, file)
