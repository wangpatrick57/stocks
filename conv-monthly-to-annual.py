#!/usr/bin/python3
# convert s&p.csv and dividends.csv to annual gain and yield
# ./conv-monthly-to-annual.py 's&p.csv' 'dividends.csv' 1928 2023 sp500-annual-gain-yield.csv

import csv
import argparse
from datetime import datetime

def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

def calculate_price_gain_and_last_year_close(annual_data):
    sorted_years = sorted(annual_data.keys())
    price_gain = {}
    last_year_close = {}

    for i in range(1, len(sorted_years)):
        previous_year = sorted_years[i - 1]
        current_year = sorted_years[i]
        previous_price = float(annual_data[previous_year])
        current_price = float(annual_data[current_year])
        gain = current_price / previous_price - 1
        price_gain[current_year] = gain
        last_year_close[current_year] = previous_price

    return price_gain, last_year_close

def read_dividends(file_path):
    dividends = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            year = datetime.strptime(row[0], '%Y-%m-%d').year
            dividends[year] = row[1]
    return dividends

def filter_annual_data(data, start_year, end_year):
    annual_data = {}
    for row in data:
        date = datetime.strptime(row['Date'], '%Y-%m-%d')
        year = date.year
        if start_year <= year <= end_year:
            # Replace the existing record for each year with the latest one
            annual_data[year] = row['Close']
    return annual_data

def write_to_csv(annual_data, price_gain, last_year_close, dividends, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Year', 'Last Year Close', 'Year-End Close Price', 'Price Gain', 'Dividend Yield'])
        for year in sorted(annual_data.keys()):
            if year in price_gain and year in last_year_close and year in dividends:
                writer.writerow([
                    year,
                    last_year_close[year],
                    annual_data[year],
                    price_gain[year],
                    dividends[year]
                ])

def main():
    parser = argparse.ArgumentParser(description='Process stock prices and dividends.')
    parser.add_argument('price_file_path', type=str, help='Path to the stock price CSV file')
    parser.add_argument('dividend_file_path', type=str, help='Path to the dividend CSV file')
    parser.add_argument('start_year', type=int, help='Start year (A)')
    parser.add_argument('end_year', type=int, help='End year (B)')
    parser.add_argument('output_file', type=str, help='Output CSV file path')
    args = parser.parse_args()

    price_data = read_csv(args.price_file_path)
    dividend_data = read_dividends(args.dividend_file_path)

    annual_prices = filter_annual_data(price_data, args.start_year, args.end_year)
    price_gain, last_year_close = calculate_price_gain_and_last_year_close(annual_prices)

    write_to_csv(annual_prices, price_gain, last_year_close, dividend_data, args.output_file)
    print(f"Processed data has been saved to {args.output_file}")

if __name__ == "__main__":
    main()
