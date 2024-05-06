import unittest
from tracker import FinanceTracker
import datetime
import os


class TestFinanceTracker(unittest.TestCase):
    def setUp(self):
        self.wallet = FinanceTracker('test_wallet.json')

    def tearDown(self):
        if os.path.exists('test_wallet.json'):
            os.remove('test_wallet.json')

    def test_add_and_edit_entry(self):
        self.wallet.add_entry(datetime.datetime.strptime('2020-10-05', "%Y-%m-%d"),
                              'Доход',
                              60000,
                              'Зарплата')
        self.assertEqual(len(self.wallet.entries), 1)

        self.wallet.edit_entry(0,
                               datetime.datetime.strptime('2020-10-05', "%Y-%m-%d"),
                               'Доход',
                               70000,
                               'Зарплата')
        self.assertEqual(self.wallet.entries[0]['Сумма'], 70000)

    def test_show_balance(self):
        self.wallet.add_entry(datetime.datetime.strptime('2020-10-05', "%Y-%m-%d"),
                              'Доход',
                              60000,
                              'Зарплата')
        self.wallet.add_entry(datetime.datetime.strptime('2020-10-07', "%Y-%m-%d"),
                              'Расход',
                              3500,
                              'Продукты на неделю')
        income, expense, balance = self.wallet.show_balance()
        self.assertEqual(income, 60000)
        self.assertEqual(expense, 3500)
        self.assertEqual(balance, 60000 - 3500)

    def test_search_entries(self):
        self.wallet.add_entry(datetime.datetime.strptime('2020-10-05', "%Y-%m-%d"),
                              'Доход',
                              60000,
                              'Зарплата')
        self.wallet.add_entry(datetime.datetime.strptime('2020-10-06', "%Y-%m-%d"),
                              'Доход',
                              50000,
                              'Премия')
        self.wallet.add_entry(datetime.datetime.strptime('2020-10-07', "%Y-%m-%d"),
                              'Расход',
                              3500,
                              'Продукты на неделю')
        self.wallet.add_entry(datetime.datetime.strptime('2020-10-08', "%Y-%m-%d"),
                              'Расход',
                              2000,
                              'Транспорт')
        self.wallet.add_entry(datetime.datetime.strptime('2020-10-09', "%Y-%m-%d"),
                              'Доход',
                              70000,
                              'Зарплата')
        self.wallet.add_entry(datetime.datetime.strptime('2020-10-10', "%Y-%m-%d"),
                              'Расход',
                              3000,
                              'Коммуналка')

        results = self.wallet.search_entries(category='Доход')
        self.assertEqual(len(results), 3)
        self.assertEqual(results, [
            {
                "Дата": "2020-10-05",
                "Категория": "Доход",
                "Сумма": 60000,
                "Описание": "Зарплата"
            },
            {
                "Дата": "2020-10-06",
                "Категория": "Доход",
                "Сумма": 50000,
                "Описание": "Премия"
            },
            {
                "Дата": "2020-10-09",
                "Категория": "Доход",
                "Сумма": 70000,
                "Описание": "Зарплата"
            }
        ])

        results = self.wallet.search_entries(category='Расход')
        self.assertEqual(len(results), 3)
        self.assertEqual(results, [
            {
                "Дата": "2020-10-07",
                "Категория": "Расход",
                "Сумма": 3500,
                "Описание": "Продукты на неделю"
            },
            {
                "Дата": "2020-10-08",
                "Категория": "Расход",
                "Сумма": 2000,
                "Описание": "Транспорт"
            },
            {
                "Дата": "2020-10-10",
                "Категория": "Расход",
                "Сумма": 3000,
                "Описание": "Коммуналка"
            }
        ])

        results = self.wallet.search_entries(date=datetime.datetime.strptime('2020-10-07', "%Y-%m-%d"))
        self.assertEqual(len(results), 1)
        self.assertEqual(results, [
            {
                "Дата": "2020-10-07",
                "Категория": "Расход",
                "Сумма": 3500,
                "Описание": "Продукты на неделю"
            }
        ])

        results = self.wallet.search_entries(amount=60000)
        self.assertEqual(len(results), 1)
        self.assertEqual(results, [
            {
                "Дата": "2020-10-05",
                "Категория": "Доход",
                "Сумма": 60000,
                "Описание": "Зарплата"
            }
        ])


if __name__ == '__main__':
    unittest.main()
