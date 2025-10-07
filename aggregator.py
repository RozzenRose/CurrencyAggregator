from rates import get_rates


class Aggregator:


    def __init__(self, data):
        self.data = data


    async def calculate(self):
        if self.data['content'] == 'Incomes':
            return await self.incomes_aggregator()
        if self.data['content'] == 'Purchases':
            return await self.purchases_aggregator()


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

        answer += euro * await get_rates('EUR', currency)
        answer += rub * await get_rates('RUB', currency)
        answer += rsd * await get_rates('RSD', currency)

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

        answer += euro * await get_rates('EUR', currency)
        answer += rub * await get_rates('RUB', currency)
        answer += rsd * await get_rates('RSD', currency)

        return {'euro': round(euro),
                'rub': round(rub),
                'rsd':round(rsd),
                'answer': round(answer)}
