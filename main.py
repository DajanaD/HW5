import asyncio
import aiohttp
from datetime import datetime, timedelta
import logging
import platform

EUR = {'EUR': {}}
USD = {'USD': {}}
list_currency = []


async def fetch_exchange_rates(session, date):
    async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?date={date}') as response:
        return await response.json()


async def parse_currency(date):
    async with aiohttp.ClientSession() as session:
        try:
            result = await fetch_exchange_rates(session, date)
            if 'exchangeRate' in result:
                list_exchangeRate = result['exchangeRate']
                eur_info = list(filter(lambda num: num['currency'] == 'EUR', list_exchangeRate))
                EUR['EUR'] = {'sale': list(map(lambda x: x['saleRate'], eur_info)),
                              'purchase': list(map(lambda x: x['purchaseRate'], eur_info))}
                usd_info = list(filter(lambda num: num['currency'] == 'USD', list_exchangeRate))
                USD['USD'] = {'sale': list(map(lambda x: x['saleRate'], usd_info)),
                              'purchase': list(map(lambda x: x['purchaseRate'], usd_info))}
                list_currency.append({date: {**EUR, **USD}})
        except aiohttp.ClientConnectorError as err:
            print(f'Connection error: {err}')


async def main(num):
    time_now = datetime.now()

    if num > 10:
        logging.info('Request exceeds 10 days')
        return list_currency

    tasks = []
    for el in range(num):
        current_time = time_now - timedelta(days=el)
        current_time = current_time.strftime("%d.%m.%Y")
        tasks.append(parse_currency(current_time))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(11))
    print(list_currency)
