import csv
import random
import time
import pandas
import pandas_datareader.data as web
import numpy
from datetime import datetime


def simple_moving_average(closes: numpy.ndarray, days: int):
    average: list[int] = []
    length = len(closes)
    for i in range(length):
        end_at = i + days - 1
        if end_at < length:
            average.append(numpy.average(closes[i: end_at]))
        else:
            average.append(-1)

    return average


def stock_slope(array: numpy.ndarray):
    slope: list[int] = []
    length = len(array)
    for i in range(length):
        if i + 1 < length and array[i] != -1:
            slope.append(array[i] - array[i + 1])
        else:
            slope.append(-1)

    return slope


def is_golden_cross(data: pandas.DataFrame):
    return data["5Slope"][0] > 0 and \
           data["5Average"][0] < data["25Average"][0] and \
           data["5Average"][0] < data["50Average"][0]
           # data['25Slope'][0] > 0 and \


def is_no_hope(data: pandas.DataFrame):
    return data["5Slope"][0] < 0


def get_stock_codes():
    codes: list[str] = []

    with open('stocks.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            codes.append(row[1])
        del codes[0]

    return codes


if __name__ == '__main__':

    with open('result.csv', "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Code"])

    fetchedStocks = pandas.read_csv('fetched.csv')
    fetched = fetchedStocks['Code'].tolist()

    no_hope_stocks = pandas.read_csv('no_hope.csv')
    no_hope = no_hope_stocks['Code'].tolist()

    st = datetime(2021, 6, 10)
    ed = datetime.now()

    stock_codes = get_stock_codes()

    for i in range(3000):
        code = stock_codes[random.randrange(0, len(stock_codes))]
        if code not in fetched and code not in no_hope:
            fetched.append(code)
            with open('fetched.csv', "a") as file:
                writer = csv.writer(file)
                writer.writerow([code])
            print(code)
            time.sleep(4)
            data = web.DataReader(code + ".JP", "stooq", st, ed)
            print(data)

            if "Close" in data.columns:
                data.loc[:, "5Average"] = simple_moving_average(data["Close"], 5)
                data.loc[:, "25Average"] = simple_moving_average(data["Close"], 25)
                data.loc[:, "50Average"] = simple_moving_average(data["Close"], 50)
                data.loc[:, "5Slope"] = stock_slope(data["5Average"])
                data.loc[:, "25Slope"] = stock_slope(data["25Average"])
                if is_golden_cross(data):
                    print(code + ": golden cross")
                    with open('result.csv', 'a') as file:
                        writer = csv.writer(file)
                        writer.writerow([code])

                if is_no_hope(data):
                    print(code + ": no hope")
                    with open('no_hope.csv', 'a') as file:
                        writer = csv.writer(file)
                        writer.writerow([code])
