import random
import math
from operator import itemgetter
from markowitz_sortino import calc_sortino, get_coins
from datetime import datetime

CRYPTO_COUNT = 10
MAX_PERCENTAGE = 0.15

def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)

letters = list(char_range('A', 'Z'))
coins = []

for x in letters:
    for y in letters:
        coins.append(x+y)

coins = get_coins()

coin_dict = {}

filtered_cryptos = [
'BKRW',
'DAI',
'FXS',
'LEND',
'VEN',
'HC',
'MCO',
'ONG',
'CLOAK',
'GNT',
'HCC',
'INS',
'SPARTA',
'CTR',
'EDO',
'EPS',
'TRIG',
'USDS',
'ARN',
'BETH',
'COS',
'DEXE',
'ERD',
'GXS',
'USDSB',
'ELC',
'ICN',
'MOD',
'PROS',
'STORM',
'BIFI',
'AUTO',
'BTG',
'BCHDOWN',
'BCHUP',
'UFT',
'BAKE',
'SLP',
'BTCB',
'TLM',
'BOT',
'PUNDIX',
'TKO',
'CFX',
'SUPER',
'RAMP',
'PERP',
'LINA',
'ALICE',
'BCHA',
'AUCTION',
'EASY',
'TVK',
'KP3R',
'DEGO',
'PROM',
'POND',
'OM',
'ACM',
'FIS',
'BADGER',
'ENG',
'POE',
'CAKE',
'DODO',
'SUB',
'NPXS',
'SFP',
'ATM',
'BCPT',
'LIT',
'FUEL',
'VIBE',
'BURGER',
'FIRO',


'PAX',
'PAXG',
'DOGE',
'GBP',
'AUD',

'DREP'
]

for coin in coins:
    if (not coin.endswith('BULL')) and (not coin.endswith('BEAR')) and (not coin.endswith('UP')) and (not coin.endswith('DOWN')) and ('USD' not in coin) and coin not in ['EUR','HC','ERD','MCO','GXS','BKRW','INS','COS','EDO', 'DAI', 'ERD', 'ICN'] \
            and coin not in filtered_cryptos:
        coin_dict[coin] = {
            'min': 0.005,
            'max': MAX_PERCENTAGE
        }

def get_value(coin):
    value = 0
    for letter in coin:
        value = value * 100 + (ord(letter) - ord('A') - 15)

    return value

def calc_total_value(dict):
    total_value = 0

    for letter, value in dict.items():
        total_value += get_value(letter) * value

    return total_value

def get_random_coins(coins, number):
    copy = coins.copy()
    random.shuffle(copy)
    return copy[:number]

def get_ramdom_value(min, max):
    value = random.uniform(min, max)
    value = round(value, 4)

    return value

def get_random_distribution(coins_dict, all_coins):
    found = False
    cant = 0
    total = 0

    selected_coins = []

    while not found:

        if cant % 1000 == 0:
            selected_coins = get_random_coins(all_coins, CRYPTO_COUNT)

        last = selected_coins[-1]

        min = coins_dict[last]['min']
        max = coins_dict[last]['max']

        cant += 1

        values = []

        for coin in selected_coins[0: -1]:
            coin_values = coins_dict[coin]

            values.append(get_ramdom_value(coin_values['min'], coin_values['max']))

        total = sum(values)

        found = total + min <= 1 <= total + max

    rest = round(1 - total, 4)
    values.append(rest)

    values.sort(reverse=True)

    result = dict(zip(selected_coins, values))

    return result


def get_top_results(coin_dict, old_top):
    coins = list(coin_dict.keys())

    data = []

    max_len = len(coins) ** 2

    # maximum max_lenght
    max_len = 10000 if max_len > 10000 else max_len

    #minimim max_lenght
    max_len = 1000 if max_len < 1000 else max_len

    for i in range(max_len):
        distribution = get_random_distribution(coin_dict, coins)

        result = {
            'distribution': distribution,
            'result': calc_sortino(distribution)
        }

        data.append(result)

    data += old_top

    sorted_data = sorted(data, key=itemgetter('result'), reverse=True)

    # top_len = int(len(coins) ** 3)
    # top_len = 10000 if top_len < 10000 else top_len

    top_len = int(max_len / 10)

    return sorted_data[0:top_len]

def rebuild_dictionary(top_values, min_number):

    new_dict = {}

    for result in top_values:
        distribution = result['distribution']

        for coin, value in distribution.items():
            if not new_dict.get(coin):
                new_dict[coin] = {
                    'coin': coin,
                    'counter': 1,
                    'min': value,
                    'max': value
                }
            else:
                element = new_dict[coin]

                element['counter'] += 1

                if value > element['max']:
                    element['max'] = value
                elif value < element['min']:
                    element['min'] = value

    sorted_data = sorted(new_dict.values(), key=itemgetter('counter'), reverse=True)

    elements_to_remove = math.floor(len(sorted_data) / 100 * 1) + 1

    if len(sorted_data) - elements_to_remove < min_number:
        filtered_data = sorted_data[0:min_number]
    else:
        filtered_data = sorted_data[0:-elements_to_remove]

    filtered_dict = {}

    for element in filtered_data:
        if len(filtered_dict.keys()) == min_number:
            element['min'] = 0.005
            element['max'] = MAX_PERCENTAGE
        else:
            element['min'] = element['min'] - 0.005 if element['min'] - 0.005 > 0.005 else 0.005
            element['max'] = element['max'] + 0.005 if element['max'] + 0.005 < MAX_PERCENTAGE else MAX_PERCENTAGE

        filtered_dict[element['coin']] = element

    return filtered_dict

def filter_top_outside_dict(top, dict):
    new_top = []

    available_coins = dict.keys()

    for t in top:
        top_coins = t['distribution'].keys()

        if len(list(set(available_coins) & set(top_coins))) == CRYPTO_COUNT:
            new_top.append(t)

    return new_top

distA = {'ZY': 0.2397, 'ZZ': 0.2385, 'ZX': 0.2354, 'ZS': 0.1262, 'ZQ': 0.0392, 'ZP': 0.0285, 'ZT': 0.0264, 'ZJ': 0.0228, 'ZM': 0.0222, 'ZN': 0.0211}
distB = {'ZZ': 0.2499, 'ZY': 0.2465, 'ZX': 0.2227, 'ZN': 0.1, 'ZQ': 0.0574, 'ZJ': 0.0369, 'ZS': 0.0329, 'ZP': 0.0238, 'ZM': 0.0211, 'ZT': 0.0264}

def compare_distribution(distA, distB):
    diff = 0

    for coin in distA.keys():
        valueA = distA[coin]
        valueB = distB.get(coin) if distB.get(coin) else 0

        diff += abs(valueA - valueB)

    for coin in distB.keys():
        if not distA.get(coin):
            diff += distB[coin]


    return diff

start = datetime.now()

top = []
new_dict = coin_dict
distribution_difference = 1

while distribution_difference > 0.01:

    top = get_top_results(new_dict, top)

    for result in top[0:10]:
        print(result)

    new_dict = rebuild_dictionary(top, min_number=CRYPTO_COUNT)

    top = filter_top_outside_dict(top, new_dict)

    print(len(new_dict))
    #print(new_dict)

    distribution_difference = compare_distribution(top[0]['distribution'], top[9]['distribution'])

    print(distribution_difference)

    print("-----------")

    if len(new_dict.keys()) > CRYPTO_COUNT * 1.5:
        top = []

print(datetime.now() - start)





