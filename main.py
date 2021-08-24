from pandas_datareader import data
import numpy


def simple_moving_average(closes: numpy.ndarray, days: int) -> list:
    average: list[int] = []
    length = len(closes)
    for i in range(length):
        end_at = i + days - 1
        if length > end_at:
            average.append(numpy.average(closes[i: end_at]))
        else:
            average.append(0)

    return average


if __name__ == '__main__':
    df = data.DataReader("1333.JP", "stooq")
    print(df["Close"].values)
    print("---------------------------------------------")
    print(simple_moving_average(df["Close"].values, 5))
