from datetime import date
from datetime import timedelta
import math

DAYS_IN_YEAR = 365
DAYS_IN_MONTH = 30

class Monkey:
    DAY_FREQUENCY = 30

    def __init__(self, earliest_date_str, latest_date_str, start_amount, stock_data, dividend_data):
        self._earliest_date = date.fromisoformat(earliest_date_str)
        self._latest_date = date.fromisoformat(latest_date_str)
        self._start_amount = start_amount
        self._stock_data = stock_data
        self._dividend_data = dividend_data

    def get_annual_return_list(self, investment_months, window_years, tax_rate):
        annual_return_list = []
        current_date = self._earliest_date
        current_end_date = current_date + timedelta(days = window_years * DAYS_IN_YEAR)

        while current_end_date <= self._latest_date:
            annual_return_list.append(self._get_annual_return(investment_months, window_years, tax_rate, current_date))
            current_date += timedelta(days = Monkey.DAY_FREQUENCY)
            current_end_date = current_date + timedelta(days = window_years * DAYS_IN_YEAR)

        return annual_return_list

    def _get_annual_return(self, investment_months, window_years, tax_rate, start_date):
        current_date = start_date
        end_date = start_date + timedelta(days = window_years * DAYS_IN_YEAR)
        current_price = -1
        owned_shares = 0
        days_since_last_investment = 0
        months_invested = 0
        last_dividend_quarter = Monkey.get_current_quarter(current_date)

        while current_date <= end_date:
            current_date_str = current_date.isoformat()

            if current_date_str in self._stock_data:
                current_price = self._stock_data[current_date_str]['adj_close']
                current_quarter = Monkey.get_current_quarter(current_date)

                # invest initial if it's the first day or it's been a month
                if months_invested < investment_months and (owned_shares == 0 or days_since_last_investment > DAYS_IN_MONTH):
                    money_to_invest = self._start_amount / investment_months
                    owned_shares += money_to_invest / current_price

                    months_invested += 1
                    days_since_last_investment = 0

                # reinvest dividends if it's a new quarter
                if current_quarter != last_dividend_quarter:
                    money_to_invest = self._dividend_data[current_date.year] / 4 * owned_shares * current_price * (1 - tax_rate)
                    owned_shares += money_to_invest / current_price
                    last_dividend_quarter = current_quarter

            days_since_last_investment += 1
            current_date += timedelta(days = 1)

        end_amount = owned_shares * current_price
        annual_return = self._calculate_annual_return(end_amount, window_years)

        if annual_return < -5:
            print(start_date, annual_return)

        return annual_return

    def _calculate_annual_return(self, end_amount, years):
        return ((end_amount / self._start_amount) ** (1 / years) - 1) * 100

    @staticmethod
    def get_current_quarter(current_date):
        if current_date.month < 3:
            return 0
        elif current_date.month == 3:
            if current_date.day <= 20:
                return 0
            else:
                return 1
        elif current_date.month < 6:
            return 1
        elif current_date.month == 6:
            if current_date.day <= 20:
                return 1
            else:
                return 2
        elif current_date.month < 9:
            return 2
        elif current_date.month == 9:
            if current_date.day <= 20:
                return 2
            else:
                return 3
        elif current_date.month < 12:
            return 3
        elif current_date.month == 12:
            if current_date.day <= 20:
                return 3
            else:
                return 0
