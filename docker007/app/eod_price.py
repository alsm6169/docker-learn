import argparse
import datetime as dt
from time import sleep

import pandas_datareader as pdr
import pandas as pd
import os
from dotenv import load_dotenv
import sqlalchemy as db
from sqlalchemy import MetaData
from sqlalchemy.sql import func

EOD_PRICE_TBL = 'eod_price'


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


def create_tables(engine: object, metadata: object) -> None:
    """
    Create a database table eod_price with columns like Date, Ticker, High....
    Parameters
    ----------
    engine: the database connection engine
    metadata: the metadata details of the database
    """
    eod_price = db.Table(EOD_PRICE_TBL, metadata,
                         db.Column('Date', db.Date(), nullable=False),
                         db.Column('Ticker', db.String(10), nullable=False),
                         db.Column('High', db.Float()),
                         db.Column('Low', db.Float()),
                         db.Column('Open', db.Float()),
                         db.Column('Close', db.Float()),
                         db.Column('Volume', db.BigInteger()),
                         db.Column('Adj Close', db.Float()),
                         db.Column('last_updated', db.DateTime(timezone=True),
                                   server_default=func.now(),
                                   onupdate=func.now(),
                                   nullable=False),
                         db.PrimaryKeyConstraint('Date', 'Ticker', name='unique_key1')
                         )

    metadata.create_all(engine)  # Creates the table


def get_db_con() -> object:
    """
    Create connection to database and then creates eod_price table if it does not exist
    Returns
    -------
    connection: the database connection engine
    engine: the metadata details of the database
    """
    load_dotenv()
    db_name = os.getenv('MYSQL_DATABASE')
    db_usr = os.getenv('MYSQL_USER')
    db_usr_pass = os.getenv('MYSQL_PASSWORD')
    db_port = os.getenv('MYSQL_DB_PORT')
    print(f'DB connection details DB_NAME: {db_name}, DB_USR_NM: {db_usr}, DB_PORT: {db_port}')
    # https://stackoverflow.com/questions/24319662/from-inside-of-a-docker-container-how-do-i-connect-to-the-localhost-of-the-mach
    # replaced localhost with host.docker.internal
    con_str = f'mysql+mysqlconnector://{db_usr}:{db_usr_pass}@host.docker.internal/{db_name}'
    print(f'con_str: {con_str}')
    engine = db.create_engine(con_str, echo=True, future=True)
    connection = engine.connect()
    metadata = db.MetaData()

    create_tables(engine, metadata)

    return connection, engine


def fetch_price(ticker: str, start_date: str, end_date: str, data_src: str, data_out: str) -> None:
    """
    Fetches the end of day data price from quandl (does not work) or yahoo finance and
    return pandas dataframe object with open, high, low close, volume etc.

    Parameters
    ----------
    ticker: the ticker whoose price has to be fetches
    start_date: begin date in YYYY-MM-DD format
    end_date: end date in YYYY-MM-DD format
    data_src: yahoo (only one value is currently accepted)
    data_out: if db then writes to database else to file in location ../output/data_out

    Returns
    -------
    None
    """
    print(f'fetch_price ticker: {ticker}, start_date: {start_date}, end_date: {end_date}, '
          f'data_src: {data_src}, data_out: {data_out}')

    # https://pandas-datareader.readthedocs.io/en/latest/remote_data.html#yahoo-finance-data
    mkt_data_df = pdr.DataReader(ticker, data_src, start_date, end_date)

    mkt_data_df.insert(0, 'Ticker', ticker)
    mkt_data_df.index = mkt_data_df.index.date
    mkt_data_df.index.rename('Date', inplace=True)
    pd.options.display.max_columns = None
    print(mkt_data_df)

    if data_out == 'db':
        connection, engine = get_db_con()
        mkt_data_df.to_sql(EOD_PRICE_TBL, engine, if_exists='append')
    else:
        print('BEFORE>files in ../output/ directory: {}'.format(os.listdir('../output/')))
        out_file_pathnm = os.path.abspath('../output/' + data_out)
        print('writing output to: {}'.format(out_file_pathnm))
        mkt_data_df.to_csv(out_file_pathnm)
        # sleep(1)
        print('AFTER>files in ../output/ directory: {}'.format(os.listdir('../output/')))


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

    # group = parser.add_mutually_exclusive_group()
    # group.add_argument('-d', '--db', action='store_true', default=False,
    #                    help='store results in DB (configuration set in .env file)')
    # group.add_argument('-f', '--file',
    #                    help='name of the csv file, e.g. out.csv')

    parser.add_argument('-d', '--db', action='store_true', default=False,
                       help='store results in DB (configuration set in .env file)')
    parser.add_argument('-f', '--file',
                       help='name of the csv file, e.g. out.csv')

    args = parser.parse_args()

    ticker = args.ticker
    print(f'__main__ ticker: {ticker}, args.begin_date: {args.begin_date}, args.end_date: {args.end_date}, '
          f', args.db: {args.db}'
          f', args.file: {args.file}')
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

    data_src = 'yahoo'
    data_out = 'db' if args.db else args.file

    fetch_price(ticker, start_date, end_date, data_src, data_out)
