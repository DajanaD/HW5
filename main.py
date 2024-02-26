import platform
from datetime import datetime, timedelta
from shlex import join
import aiohttp
import asyncio
import logging

EUR = {'EUR': {}}
USD = {'USD': {}}
list_currency = []


# async def period():
#     time_now =datetime.now()
#     for el in range():
#         current_time = time_now + timedelta(days=el)
#         current_time.strftime("%d.%m.%Y")

async def main(num):    
    time_now =datetime.now()
    if num >10:    # проверка на превышение 10 дней
       return logging.info('request exceeds 10 days')
    for el in range(num):    # итерация по дням
        current_time = time_now - timedelta(days=el)
        current_time = current_time.strftime("%d.%m.%Y")
   
        async with aiohttp.ClientSession() as session: # получчение данных с сайта
            try:
                async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?date={current_time}') as response:
                    result = await response.json()
                    # return result
                    for key, value in result.items(): # формирование списка словарей
                        if key == 'exchangeRate':
                            list_exchangeRate = value
                            eur_info = list(filter(lambda num: num['currency'] == 'EUR', list_exchangeRate))
                            EUR['EUR'] = {'sale':list(map(lambda x : x['saleRate'], eur_info)), 'purchase':list(map(lambda x : x['purchaseRate'], eur_info))}
                            usd_info = list(filter(lambda num: num['currency'] == 'USD', list_exchangeRate))
                            USD['USD'] = {'sale':list(map(lambda x : x['saleRate'], usd_info)), 'purchase':list(map(lambda x : x['purchaseRate'], eur_info))}
                            # for el in EUR['EUR']:
                                # el['sale'] = [float(x) for x in el['sale']]
                            list_currency.append({current_time:{**EUR, **USD}})
                return list_currency
            except aiohttp.ClientConnectorError as err:
                print(f'Connection error', str(err))
                  
                    
        

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main(11))
    print(r)
