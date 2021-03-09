import json
from datetime import date
from input_helpers import *
from processing_helpers import *
import statistics

START_AMOUNT = 10000
EARLIEST_DATE_STR = '1927-12-30'
LATEST_DATE_STR = '2020-12-31'

def calculate_annual_return(start_amount, end_amount, years):
    return ((end_amount / start_amount) ** (1 / years) - 1) * 100

def output_str_format(end_amount, start_amount, years):
    return f'${end_amount:.0f} –– {calculate_annual_return(start_amount, end_amount, years):.2f}%'

def print_list_analytics(end_amount_list, start_amount, years):
    mean = statistics.mean(end_amount_list)
    median = statistics.median(end_amount_list)
    stdev = statistics.stdev(end_amount_list)
    list_min = min(end_amount_list)
    list_max = max(end_amount_list)
    print(f'mean: {output_str_format(mean, start_amount, years)}')
    print(f'median: {output_str_format(median, start_amount, years)}')
    print(f'stdev: {output_str_format(stdev, start_amount, years)}')
    print(f'min: {output_str_format(list_min, start_amount, years)}')
    print(f'max: {output_str_format(list_max, start_amount, years)}')

def print_list_title(investment_months, window_years, tax_rate):
    print(f'{investment_months} months | {window_years} years | {tax_rate * 100}% tax')

def main():
    stock_data_file = open('s&p.csv', 'r')
    dividend_data_file = open('dividends.csv', 'r')
    stock_data = get_stock_data(stock_data_file)
    dividend_data = get_dividend_data(dividend_data_file)

    monkey = Monkey(EARLIEST_DATE_STR, LATEST_DATE_STR, START_AMOUNT, stock_data, dividend_data)

    for investment_months in [1, 3, 6, 12, 24, 36]:
        for window_years in [30]:
            for tax_rate in [0.4]:
                end_amount_list = monkey.get_end_amount_list(investment_months, window_years, tax_rate)
                print_list_title(investment_months, window_years, tax_rate)
                print_list_analytics(end_amount_list, START_AMOUNT, window_years)
                print()

if __name__ == '__main__':
    main()
