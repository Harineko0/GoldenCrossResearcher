import csv

from pandas_datareader import data
import numpy


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


if __name__ == '__main__':
    stock_code: list[str] = []
    with open('stocks.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            stock_code.append(row[1])
        del stock_code[0]

    print(stock_code)

    df = data.DataReader("7820.JP", "stooq")
    df.loc[:, "25Average"] = simple_moving_average(df["Close"], 25)
    df.loc[:, "50Average"] = simple_moving_average(df["Close"], 50)
    df.loc[:, "5Average"] = simple_moving_average(df["Close"], 5)
    df.loc[:, "5Slope"] = stock_slope(df["5Average"])
