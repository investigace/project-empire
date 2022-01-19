import decimal

def convert_currency(from_amount, from_currency, to_currency, year):
    if from_currency == 'CZK' and to_currency == 'EUR':
        return convert_czk_to_eur(from_amount, year)
    else:
        raise Exception(f'Non implemented currency exchange from {from_currency} to {to_currency}')

def convert_czk_to_eur(amount, year):
    if amount is None or year is None:
        return (None, None)

    rate_year = int(year)
    
    # Euro started on Jan 1st, 1999, so for anything before we will use year 1999
    if rate_year < 1999:
        rate_year = 1999
    
    rates = {
        '2021': 25.640,
        '2020': 26.455,
        '2019': 25.670,
        '2018': 25.647,
        '2017': 26.326,
        '2016': 27.034,
        '2015': 27.279,
        '2014': 27.536,
        '2013': 25.980,
        '2012': 25.149,
        '2011': 24.590,
        '2010': 26.284,
        '2009': 26.435,
        '2008': 24.946,

        '2007': 26.829,
        '2006': 28.045,
        '2005': 29.298,
        '2004': 31.126,
        '2003': 32.089,
        '2002': 30.853,
        '2001': 33.202,
        '2000': 34.911,
        '1999': 36.340,
    }

    if not str(rate_year) in rates:
        return (None, None)

    rate = rates[str(rate_year)]

    if rate_year >= 2008:
        note = f"Částka v EUR dle kurzu CZK/EUR {rate:.3f} z roku {rate_year}. Zdroj: Směnné kurzy dle jednotlivých let zveřejněné na serveru Eurostat. Dostupné z: https://ec.europa.eu/eurostat/web/exchange-and-interest-rates/data/database"
    else:
        note = f"Částka v EUR dle kurzu CZK/EUR {rate:.3f} z roku {rate_year}. Zdroj: Devízové kurzy vedené Českou národní bankou. Dostupné z: https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/prumerne_form.html"

    return (
        round(decimal.Decimal(amount) / decimal.Decimal(rate)),
        note
    )
