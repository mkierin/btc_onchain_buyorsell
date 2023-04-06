import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

API_KEY = os.getenv("API_KEY")

headers = {
    'Authorization': 'Bearer ' + API_KEY
}


from datetime import datetime, timedelta

def get_puell_multiple():
    base_url = "https://api.cryptoquant.com/v1/btc/network-indicator/puell-multiple?window=day&from={}&limit=2000"
    return fetch_all_data(base_url, 'puell_multiple')

def get_mvrv():
    base_url = "https://api.cryptoquant.com/v1/btc/market-indicator/mvrv?window=day&from={}&limit=2000"
    return fetch_all_data(base_url, 'mvrv')

def get_nupl():
    base_url = "https://api.cryptoquant.com/v1/btc/network-indicator/nupl?window=day&from={}&limit=2000"
    return fetch_all_data(base_url, 'nupl')

def fetch_all_data(base_url, key):
    data = []
    date = datetime.now()
    while True:
        url = base_url.format(date.strftime('%Y%m%d'))
        response = requests.get(url, headers=headers)
        json_data = response.json()
        print(f"Raw data for {key}:")
        print(json_data)
        if not json_data['result']['data']:
            break
        data.extend(json_data['result']['data'])
        date -= timedelta(days=2000)
    return {'status': json_data['status'], 'result': {'window': 'day', 'data': data}}

if __name__ == "__main__":
    print(get_puell_multiple())
    print(get_mvrv())
    print(get_nupl())


def process_metric_data(data, key):
    if not data:
        return {
            'current_value': None,
            'highest_value': None,
            'lowest_value': None,
            'distance_from_top': None,
            'risk': 'No data available'
        }

    current_value = round(data[0][key], 2)
    highest_value = round(max(data, key=lambda x: x[key])[key], 2)
    lowest_value = round(min(data, key=lambda x: x[key])[key], 2)
    distance_from_top = round(((highest_value - current_value) / (highest_value - lowest_value)) * 100, 2)

    risk = ''

    if distance_from_top <= 50:
        risk = 'Great time to sell'
    elif distance_from_top >= 80:
        risk = 'Great time to buy'
    else:
        risk = 'Uncertain'

    return {
        'current_value': current_value,
        'highest_value': highest_value,
        'lowest_value': lowest_value,
        'distance_from_top': distance_from_top,
        'risk': risk
    }



def get_puell_multiple_data():
    raw_data = get_puell_multiple()
    data = raw_data['result']['data']
    return process_metric_data(data, 'puell_multiple')

def get_mvrv_data():
    raw_data = get_mvrv()
    data = raw_data['result']['data']
    return process_metric_data(data, 'mvrv')

def get_nupl_data():
    raw_data = get_nupl()
    data = raw_data['result']['data']
    return process_metric_data(data, 'nupl')


def get_recommendation(puell_multiple, mvrv, nupl):
    if puell_multiple is None or mvrv is None or nupl is None:
        return 'No data available for making a recommendation.'

    recommendation = ''

    if mvrv < 1:
        recommendation += 'MVRV is low (<1), indicating an undervalued market. '
    elif mvrv > 2:
        recommendation += 'MVRV is high (>2), indicating an overvalued market. '

    if nupl < 0:
        recommendation += 'NUPL is negative, meaning more investors are at a loss. '
    elif nupl > 0:
        recommendation += 'NUPL is positive, meaning more investors are at a profit. '

    if recommendation:
        recommendation += 'Based on these factors, it might be a good time to '
        if mvrv < 1 and nupl < 0:
            recommendation += 'buy Bitcoin.'
        elif mvrv > 2 and nupl > 0:
            recommendation += 'sell Bitcoin.'
        else:
            recommendation = 'The market situation is uncertain. Please analyze further before making a decision.'
    
    return recommendation


    
