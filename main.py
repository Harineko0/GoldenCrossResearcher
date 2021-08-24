import csv

import pandas
from pandas_datareader import data
import pandas_datareader.data as web
import numpy
from datetime import datetime

from config import api_key


def simple_moving_average(closes: numpy.ndarray, days: int) -> list[int]:
    average: list[int] = []
    length = len(closes)
    for i in range(length):
        end_at = i + days - 1
        if end_at < length:
            average.append(numpy.average(closes[i: end_at]))
        else:
            average.append(-1)

    return average


def stock_slope(array: numpy.ndarray) -> list[int]:
    slope: list[int] = []
    length = len(array)
    for i in range(length):
        if i + 1 < length and array[i] != -1:
            slope.append(array[i] - array[i + 1])
        else:
            slope.append(-1)

    return slope


def golden_cross(data_frame: pandas.DataFrame) -> bool:
    return data_frame["5Slope"][0] > 0 and data_frame["5Average"][0] < data_frame["25Average"][0] and \
           data_frame["5Average"][0] < data_frame["50Average"][0]


def get_stock_codes() -> list[str]:
    codes: list[str] = []
    with open('stocks.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            codes.append(row[1])
        del codes[0]

    return codes


if __name__ == '__main__':
    stock_codes = get_stock_codes()

    golden_cross_stocks: list[str] = []
    st = datetime(2021, 6, 10)
    ed = datetime(2021, 8, 24)

    for code in stock_codes:
        df = web.DataReader(code + ".JP", "stooq", st, ed, api_key=api_key)
        if "Close" in df.columns:
            df.loc[:, "5Average"] = simple_moving_average(df["Close"], 5)
            df.loc[:, "25Average"] = simple_moving_average(df["Close"], 25)
            df.loc[:, "50Average"] = simple_moving_average(df["Close"], 50)
            df.loc[:, "5Slope"] = stock_slope(df["5Average"])
            print(code)
            print(df)
            if golden_cross(df):
                print(code + ": golden cross")
                golden_cross_stocks.append(code)

    print(golden_cross_stocks)
