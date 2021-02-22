import json
from datetime import date
from input_helpers import *
from processing_helpers import *
import statistics

START_AMOUNT = 10000
EARLIEST_DATE_STR = '1927-12-30'
LATEST_DATE_STR = '2020-12-30'

def print_list_analytics(annual_return_list):
    mean = statistics.mean(annual_return_list)
    median = statistics.median(annual_return_list)
    stdev = statistics.stdev(annual_return_list)
    list_min = min(annual_return_list)
    list_max = max(annual_return_list)
    print(f'mean: {mean}')
    print(f'median: {median}')
    print(f'stdev: {stdev}')
    print(f'min: {list_min}')
    print(f'max: {list_max}')

def print_list_title(investment_months, window_years, tax_rate):
    print(f'{investment_months} months | {window_years} years | {tax_rate * 100}% tax')

def main():
    stock_data_file = open('s&p.csv', 'r')
    dividend_data_file = open('dividends.csv', 'r')
    stock_data = get_stock_data(stock_data_file)
    dividend_data = get_dividend_data(dividend_data_file)

    monkey = Monkey(EARLIEST_DATE_STR, LATEST_DATE_STR, START_AMOUNT, stock_data, dividend_data)

    for investment_months in [1]:
        for window_years in [30]:
            for tax_rate in [1]:
                annual_return_list = monkey.get_annual_return_list(investment_months, window_years, tax_rate)
                print_list_title(investment_months, window_years, tax_rate)
                print_list_analytics(annual_return_list)
                print()

if __name__ == '__main__':
    main()
