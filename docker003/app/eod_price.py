import argparse
import datetime as dt
import pandas_datareader as pdr
import nasdaqdatalink as ndl
import pandas as pd
import os


def validate_date(date_text: str) -> bool:
    """
    Check if the date_text is string in format YYYY-MM-DD and it converts to valid date.
    i.e. 31-01-2001 returns True, 30-02-2002 returns False, 30.01.2010 returns False

    Parameters
    ----------
    date_text: String to check if it is a valid date and in format YYYY-MM-DD

    Returns
    -------
    True: if string can be converted to a valid date else False

    """
    try:
        dt.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        print(f'Incorrect data format: {date_text}, should be YYYY-MM-DD')
        return False


def fetch_price(ticker: str, start_date: str, end_date: str, data_src: str, file_name: str) -> object:
    """
    Fetches the end of day data price from quandl (does not work) or yahoo finance and
    return pandas dataframe object with open, high, low close, volume etc.

    Parameters
    ----------
    ticker: the ticker whoose price has to be fetches
    start_date: begin date in YYYY-MM-DD format
    end_date: end date in YYYY-MM-DD format
    data_src: string = quandl (DOES NOT WORK) / yahoo
    file_name: output file name

    Returns
    -------
    pandas dataframe: with  open, high, low close, volume etc.
    """
    print(f'fetch_price ticker: {ticker}, start_date: {start_date}, end_date: {end_date}, '
          f'data_src: {data_src}, file_name: {file_name}')

    if data_src == 'quandl':
        # https://docs.data.nasdaq.com/docs/python-time-series
        ndl.ApiConfig.api_key = os.environ['NASDAQ_DATA_LINK_API_KEY']
        # mkt_data_df = ndl.Dataset('WIKI/' + ticker).data().to_pandas()
        # mkt_data_df = ndl.get('WIKI/' + ticker, rows=5)
        # mkt_data_df = ndl.get('WIKI/' + ticker, start_date=start_date, end_date=end_date)
        print('QUANDL DOES NOT WORK CURRENTLY')
        mkt_data_df = pd.DataFrame()
    else:
        # https://pandas-datareader.readthedocs.io/en/latest/remote_data.html#yahoo-finance-data
        mkt_data_df = pdr.DataReader(ticker, data_src, start_date, end_date)

    mkt_data_df.insert(0, 'ticker', ticker)
    pd.options.display.max_columns = None
    print(mkt_data_df)

    if file_name is not None:
        mkt_data_df.to_csv('../output/'+file_name)


if __name__ == '__main__':
    print(f'os.getcwd: {os.getcwd()}')
    parser = argparse.ArgumentParser()
    parser.add_argument('ticker', type=str, nargs='?', default='MSFT',
                        help='echo back the input message')
    parser.add_argument('-b', '--begin_date', type=str, default=None,
                        help='Start date (YYYY-MM-DD) / '
                             'number of days in the past to include [default: 1 i.e. last working day]')
    parser.add_argument('-e', '--end_date', type=str, default=None,
                        help='Latest date (YYYY-MM-DD) to include [default: today]')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q', '--quandl', action='store_true', default=False,
                       help='Data Source is Quandl (DOES NOT WORK CURRENTLY)')
    group.add_argument('-y', '--yahoo', action='store_true', default=True,
                       help='Data Source is Yahoo')

    parser.add_argument('-f', '--file',
                        help='name of the csv file, e.g. out.csv')

    args = parser.parse_args()

    ticker = args.ticker
    print(f'__main__ ticker: {ticker}, args.begin_date: {args.begin_date}, args.end_date: {args.end_date}, '
          f'quandl: {args.quandl}, yahoo: {args.yahoo}, args.file: {args.file}')
    if args.begin_date is None:
        start_date = (dt.date.today() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        if args.begin_date.isnumeric():
            num_days = int(args.begin_date)
            start_date = (dt.date.today() - dt.timedelta(days=num_days)).strftime("%Y-%m-%d")
        elif not validate_date(args.begin_date):
            start_date = (dt.date.today() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            start_date = args.begin_date

    if args.end_date is None or not validate_date(args.begin_date):
        end_date = dt.date.today().strftime("%Y-%m-%d")
    else:
        end_date = args.end_date

    data_src = 'quandl' if args.quandl else 'yahoo'

    fetch_price(ticker, start_date, end_date, data_src, args.file)
