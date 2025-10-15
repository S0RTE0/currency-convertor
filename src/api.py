from dataclasses import dataclass
import requests

ALL_CURRENCIES_URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies"

@dataclass
class Api:
    def get_all_currencies(self):
        response = requests.get(ALL_CURRENCIES_URL + ".json").json()
        lst = []
        for code in response:
            lst.append(code)
        return lst
    
    def get_currency(self, currency_from: str, currency_to: str, target: float):
        response = requests.get(f"{ALL_CURRENCIES_URL}/{currency_from}.min.json").json()
        return response[currency_from][currency_to] * target
