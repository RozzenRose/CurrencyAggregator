from logic.rates import get_rates


class Aggregator:


    def __init__(self, data):
        self.data = data


    async def calculate(self):
        self.eur = await get_rates('EUR')
        self.rub = await get_rates('RUB')
        self.rsd = await get_rates('RSD')
        if self.data['content'] == 'Incomes':
            return await self.incomes_aggregator()
        if self.data['content'] == 'Purchases':
            return await self.purchases_aggregator()
        if self.data['content'] == 'Report':
            return await self.report_aggregator()


    async def report_aggregator(self):
        data = self.data['data']
        currency = data['current_currency']
        for item in data['purchases']:
            if item['currency'] == 'EUR':
                item['price'] = item['price'] * self.eur.get(currency, 1)
            if item['currency'] == 'RUB':
                item['price'] = item['price'] * self.rub.get(currency, 1)
            if item['currency'] == 'RSD':
                item['price'] = item['price'] * self.rsd.get(currency, 1)
            item['currency'] = currency

        for item in data['incomes']:
            if item['currency'] == 'EUR':
                item['quantity'] = item['quantity'] * self.eur.get(currency, 1)
            if item['currency'] == 'RUB':
                item['quantity'] = item['quantity'] * self.rub.get(currency, 1)
            if item['currency'] == 'RSD':
                item['quantity'] = item['quantity'] * self.rsd.get(currency, 1)
            item['currency'] = currency

        return data


    async def purchases_aggregator(self):
        numbers = [(item['price'], item['currency']) for item in self.data['purchases']]
        currency = self.data['current_currency']
        euro, rub, rsd = 0, 0, 0
        answer = 0

        for number in numbers:
            if number[1] == 'EUR':
                euro += number[0]
            if number[1] == 'RUB':
                rub += number[0]
            if number[1] == 'RSD':
                rsd += number[0]

        answer += euro * self.eur.get(currency, 1)
        answer += rub * self.rub.get(currency, 1)
        answer += rsd * self.rsd.get(currency, 1)

        return {'euro': round(euro),
                'rub': round(rub),
                'rsd':round(rsd),
                'answer': round(answer)}


    async def incomes_aggregator(self):
        numbers = [(item['quantity'], (item['currency'])) for item in self.data['incomes']]
        currency = self.data['current_currency']
        euro, rub, rsd = 0, 0, 0
        answer = 0

        for number in numbers:
            if number[1] == 'EUR':
                euro += number[0]
            if number[1] == 'RUB':
                rub += number[0]
            if number[1] == 'RSD':
                rsd += number[0]

        answer += euro * self.eur.get(currency, 1)
        answer += rub * self.rub.get(currency, 1)
        answer += rsd * self.rsd.get(currency, 1)

        return {'euro': round(euro),
                'rub': round(rub),
                'rsd':round(rsd),
                'answer': round(answer)}
