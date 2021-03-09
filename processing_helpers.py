from datetime import date
from datetime import timedelta
import math

def get_current_quarter(current_date):
    if current_date.month <= 3:
        return 0
    elif current_date.month <= 6:
        return 1
    elif current_date.month <= 9:
        return 2
    elif current_date.month <= 12:
        return 3

def get_start_month_date(base_date):
    if base_date.day == 1:
        return base_date
    else:
        return get_next_month_date(base_date)

def get_next_month_date(base_date):
    if base_date.month == 12:
        return date(base_date.year + 1, 1, 1)
    else:
        return date(base_date.year, base_date.month + 1, 1)

def get_start_quarter_date(base_date):
    if base_date.month >= 10:
        return date(base_date.year + 1, 1, 1)
    else:
        if base_date.month <= 3:
            quarter_month = 4
        elif base_date.month <= 6:
            quarter_month = 7
        elif base_date.month <= 9:
            quarter_month = 10

        return date(base_date.year, quarter_month, 1)

def get_next_quarter_date(base_date):
    if base_date.month == 10:
        return date(base_date.year + 1, 1, 1)
    else:
        return date(base_date.year, base_date.month + 3, 1)

class Monkey:
    DAY_FREQUENCY = 1

    def __init__(self, earliest_date_str, latest_date_str, start_amount, stock_data, dividend_data):
        self._earliest_date = date.fromisoformat(earliest_date_str)
        self._latest_date = date.fromisoformat(latest_date_str)
        self._start_amount = start_amount
        self._stock_data = stock_data
        self._dividend_data = dividend_data

    def get_end_amount_list(self, investment_months, window_years, tax_rate):
        end_amount_list = []
        current_date = self._earliest_date
        current_end_date = date(current_date.year + window_years, current_date.month, current_date.day)

        while current_end_date <= self._latest_date:
            end_amount_list.append(self._get_end_amount(investment_months, window_years, tax_rate, current_date))
            current_date += timedelta(days = Monkey.DAY_FREQUENCY)

            if current_date.month == 2 and current_date.day == 29:
                current_date += timedelta(days = 1)

            current_end_date = date(current_date.year + window_years, current_date.month, current_date.day)

        return end_amount_list

    def _get_end_amount(self, investment_months, window_years, tax_rate, start_date):
        end_date = date(start_date.year + window_years, start_date.month, start_date.day)
        current_price = -1
        owned_shares = 0
        months_invested = 0
        last_dividend_quarter = get_current_quarter(start_date - timedelta(days = 1))
        jump_dates = []

        # add months
        for i in range(investment_months):
            if i == 0:
                jump_dates.append(get_start_month_date(start_date))
            else:
                jump_dates.append(get_next_month_date(jump_dates[-1]))

        # add dividends
        curr_dividend_date = get_start_quarter_date(jump_dates[-1])

        while curr_dividend_date < end_date:
            jump_dates.append(curr_dividend_date)
            curr_dividend_date = get_next_quarter_date(curr_dividend_date)

        for current_date in jump_dates:
            current_date_str = current_date.isoformat()

            while current_date_str not in self._stock_data and current_date <= self._latest_date:
                current_date += timedelta(days = 1)
                current_date_str = current_date.isoformat()

            if current_date > self._latest_date:
                break

            current_price = self._stock_data[current_date_str]['adj_close']
            current_quarter = get_current_quarter(current_date)

            # invest initial if that hasn't happened enough yet
            if months_invested < investment_months:
                money_to_invest = self._start_amount / investment_months
                owned_shares += money_to_invest / current_price

                months_invested += 1
                days_since_last_investment = 0

            # reinvest dividends if it's a new quarter
            if current_quarter != last_dividend_quarter:
                dividend_year_to_use = current_date.year

                while dividend_year_to_use not in self._dividend_data:
                    dividend_year_to_use -= 1

                money_to_invest = self._dividend_data[dividend_year_to_use] / 4 * owned_shares * current_price * (1 - tax_rate)
                owned_shares += money_to_invest / current_price
                last_dividend_quarter = current_quarter

        end_amount = owned_shares * current_price

        return end_amount
