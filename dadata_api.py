import json
import requests
import argparse

from dadata_db import create_db, add_table_values


def check_token_validity(api_key):
    url_check_token = 'https://dadata.ru/api/suggest/address/'
    headers = {'Authorization': 'Token %s' % api_key}
    response = requests.get(url_check_token, headers=headers)
    return response.ok


def get_dadata_locations(base_url, api_key, language, query, resource):
    base_url = base_url % resource
    headers = {
        'Authorization': 'Token %s' % api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'query': query,
        'language': language
    }

    r = requests.post(base_url, data=json.dumps(data), headers=headers)
    data = r.json()
    return data


def get_addresses(data):
    result = []
    for location in data['suggestions']:
        result.append(location.get('unrestricted_value'))
    return result


def get_longitude(data, index):
    return data['suggestions'][index]['data']['geo_lon']


def get_latitude(data, index):
    return data['suggestions'][index]['data']['geo_lat']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("api_key", help="API-key from Dadata")
    args = parser.parse_args()
    api_key = args.api_key

create_db()
answer = 2
try:
    answer = int(input("""Выберите опцию:
    0 - Сделать запрос
    1 - Сменить язык Ru/Eng
    2 - Выход
Выбор: """))
    if answer != 2:
        if check_token_validity(api_key):
            language = 'ru'
            if answer == 1:
                lang = int(
                    input('Изменить язык на анлийский? 1 - Да \n2 - Нет\nВыбор: '))
                if lang == 1:
                    language = 'en'
                    print('Language changed')
                else:
                    print('Язык не изменен')
                    answer = 2
            settings = add_table_values(api_key, language)
            base_url, api_key, language = settings[0], settings[1], settings[2]
except ValueError:
    print("\nОшибка, возможно Вы ввели некорректные данные.")
except KeyboardInterrupt:
    print("\nПрограмма прервана пользователем.")
except EOFError:
    print("\nОшибка. EOFError received")
except TypeError as e:
    print(f"Error: {e}")
except Exception as e:
    print('Нам очень жаль, произошла ошибка: ', e)


while answer != 2:
    try:
        query = input('Введите поисковый запрос: ')
        if query.isalpha():
            data = get_dadata_locations(
                base_url=base_url, api_key=api_key, language=language, query=query, resource='address')
            adresses = get_addresses(data)
            for idx, location in enumerate(adresses):
                print(idx, "- ", location)

            locationIdx = int(input('Укажите номер адреса из списка: '))

            latitude = None
            longitude = None

            try:
                latitude = get_latitude(data, locationIdx)
                longitude = get_longitude(data, locationIdx)
            except IndexError:
                print("Ошибка. Введённый номер должен быть в диапазоне значений.")
            if latitude is not None and longitude is not None:
                print('Широта: ', latitude, ", Долгота: ", longitude)
            answer = int(input('1 - Продолжить \n2 - Выйти\nВыбор: '))
        else:
            print('Неверный формат поискового запроса')
            answer = int(input('1 - Продолжить \n2 - Выйти: \nВыбор: '))
    except ValueError:
        print("\nValue error received")
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received")
    except EOFError:
        print("\nEOFError received")
    except TypeError as e:
        print(f"Error: {e}")
