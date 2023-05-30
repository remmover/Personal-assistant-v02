from datetime import datetime

from pyowm import OWM, commons
import requests


def exchange_rates():
    bank_ua_responce = requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json')
    privat_response = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5')
    data_bank, data_privat = bank_ua_responce.json(), privat_response.json()
    usd_privat_buy, usd_privat_sale = float(data_privat[1]['buy']), float(data_privat[1]['sale'])
    eur_privat_buy, eur_privat_sale = float(data_privat[0]['buy']), float(data_privat[0]['sale'])
    eur_bank_rate = float(data_bank[31]['rate'])
    usd_bank_rate = float(data_bank[24]['rate'])
    current_date = datetime.now().date().strftime('%d-%m-%Y')
    
    return f'\n\tПоточний курс на {current_date} згідно з Готівковим курсом Приватбанку:\n\
        \tUSD:\tКупівля = {usd_privat_buy:.3f}грн\tПродаж = {usd_privat_sale:.3f}грн\n\
        \tEUR:\tКупівля = {eur_privat_buy:.3f}грн\tПродаж = {eur_privat_sale:.3f}грн\n\
        \n\tЗгідно з Національним банком України:\n\
        \tUSD:\t{usd_bank_rate:.3f}грн\
        \tEUR:\t{eur_bank_rate:.3f}грн'

def show_weather():
    while True:
        try:
            user_input = input('Введи українською назву міста:\n>>> ').capitalize()
            manager = OWM('84061a2a5ff54b490d63bd38d557b06d').weather_manager()
            observation = manager.weather_at_place(user_input)
            weather = observation.weather
            status = weather.detailed_status
            wind = weather.wind()['speed']
            temp_now, feel = weather.temperature('celsius')['temp'], weather.temperature('celsius')['feels_like'] 
            match status:
                case 'clear sky':
                    status = 'ясно'
                case 'overcast clouds':
                    status = 'хмарно'
                case 'broken clouds':
                    status = 'перемінна хмарність'
                case 'few clouds', 'scattered clouds':
                    status = 'малохмарно'
                case 'light rain', 'moderate rain', 'heavy intensity rain', 'very heavy rain', 'extreme rain', 'freezing rain', 'light intensity shower rain', 'shower rain', 'heavy intensity shower rain':
                    status = 'дощ'
                case 'light snow', 'moderate snow', 'heavy snow', 'sleet', 'light shower sleet', 'shower sleet', "shower snow", 'heavy shower snow':
                    status = 'сніг'
                case 'rain and snow', 'light shower snow', 'light rain and snow':
                    status = 'сніг з дощем'
                case 'thunderstorm with light rain', 'thunderstorm with rain', 'thunderstorm with heavy rain', 'light thunderstorm', 'thunderstorm', 'heavy thunderstorm', 'ragged thunderstorm', 'thunderstorm with light drizzle', 'thunderstorm with drizzle', 'thunderstorm with heavy drizzle':
                    status = 'гроза'
                case 'mist', 'smoke', 'haze', 'sand/ dust whirls', 'fog', 'sand', 'dust':
                    status = 'туман'

            return f'\nНа даний момент у місті {user_input} {status}\n\
Температура зараз {temp_now}°C\n\
Відчувається як {feel}°C\n\
Швидкість вітру: {wind}м/с\n'

        except commons.exceptions.NotFoundError:
            print('\nТи ввів місто неправильно, спробуй ще раз.\n')
