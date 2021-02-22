from datetime import date

def get_stock_data(stock_data_file):
    stock_data = dict()

    for i, line in enumerate(stock_data_file):
        split_line = line.strip().split(',')

        if i == 0:
            field_names = [raw_field_name.replace(' ', '_').lower() for raw_field_name in split_line]
        else:
            date_str = split_line[0]
            stock_data[date_str] = dict()

            for j in range(1, len(split_line)):
                stock_data[date_str][field_names[j]] = float(split_line[j])

    return stock_data

def get_dividend_data(dividend_data_file):
    dividend_data = dict()

    for line in dividend_data_file:
        split_line = line.strip().split(',')
        date_str = split_line[0]
        date_obj = date.fromisoformat(date_str)
        dividend_data[date_obj.year] = float(split_line[1])

    return dividend_data
