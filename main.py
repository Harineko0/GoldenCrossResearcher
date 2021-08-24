from pandas_datareader import data
import numpy


def simple_moving_average(closes: numpy.ndarray, days: int) -> list:
    average = []
    for i in range(len(closes)):
        numpy.average()


if __name__ == '__main__':
    df = data.DataReader("1333.JP", "stooq")
    print(df["Close"].values)
