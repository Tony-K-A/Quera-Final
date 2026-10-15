from Bank import API

_api = API()

def pay(card, exp_month, exp_year, password, cvv2, amount):
    return _api.pay(card, exp_month, exp_year, password, cvv2, amount)
