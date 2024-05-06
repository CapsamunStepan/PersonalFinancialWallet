import os
import json
import datetime
from typing import List, Dict, Optional, Tuple


class FinanceTracker:
    """
    Этот класс предоставляет возможность отслеживать финансовые операции, такие как добавление, редактирование, поиск
    записей и отображение баланса.

    Атрибуты:
        - entries: Optional[List[Dict[str, str]]]: Список словарей, представляющих финансовые записи. Каждая запись
        содержит информацию о дате, категории, сумме и описании операции. Может быть None, если записи еще не загружены.
        - file_path: str: Путь к файлу, в котором сохранены финансовые записи.

    Методы:
        - __init__(file_path: str): Конструктор класса. Инициализирует атрибуты и загружает записи из файла.
        - load_entries(): Загружает финансовые записи из файла.
        - save_entries(): Сохраняет текущие финансовые записи в файл.
        - add_entry(date: datetime.datetime, category: str, amount: float, description: str): Добавляет новую
        финансовую запись.
        - edit_entry(index: int, date: datetime.datetime, category: str, amount: float, description: str): Редактирует
        существующую финансовую запись по индексу.
        - search_entries(category: Optional[str] = None, date: Optional[datetime.datetime] = None,
        amount: Optional[float] = None) -> List[Dict[str, str]]: Выполняет поиск финансовых записей
        по заданным критериям.
        - show_balance() -> Tuple[float, float, float]: Отображает текущий баланс, сумму доходов и расходов,
        а также возвращает их значения в виде кортежа.

    Пожалуйста, обратите внимание, что для успешной работы некоторых методов требуется модуль datetime и json.
    """
    def __init__(self, file_path: str):
        """
        Конструктор класса FinanceTracker.

        Параметры:
            - file_path: str: Путь к файлу, в котором сохранены финансовые записи.
        """
        self.entries: Optional[List[Dict[str, str]]] = None
        self.file_path: str = file_path
        self.load_entries()

    def load_entries(self) -> None:
        """
        Загружает финансовые записи из файла.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                self.entries = json.load(file)
        else:
            self.entries = []

    def save_entries(self) -> None:
        """
        Сохраняет текущие финансовые записи в файл.
        """
        with open(self.file_path, 'w') as file:
            json.dump(self.entries, file, ensure_ascii=False, indent=4)

    def add_entry(self, date: datetime.datetime, category: str, amount: float, description: str) -> None:
        """
        Добавляет новую финансовую запись.

        Параметры:
            - date: datetime.datetime: Дата операции.
            - category: str: Категория операции (например, "Доход" или "Расход").
            - amount: float: Сумма операции.
            - description: str: Описание операции.
        """
        try:
            new_entry = {
                "Дата": date.strftime("%Y-%m-%d"),
                "Категория": category,
                "Сумма": amount,
                "Описание": description
            }
            self.entries.append(new_entry)
            self.save_entries()
        except Exception as e:
            print(f"Ошибка при добавлении записи: {e}")

    def edit_entry(self, index: int, date: datetime.datetime, category: str, amount: float, description: str) -> None:
        """
        Редактирует существующую финансовую запись по индексу.

        Параметры:
            - index: int: Индекс записи, которую нужно отредактировать.
            - date: datetime.datetime: Новая дата операции.
            - category: str: Новая категория операции.
            - amount: float: Новая сумма операции.
            - description: str: Новое описание операции.
        """
        try:
            self.entries[index] = {
                "Дата": date.strftime("%Y-%m-%d"),
                "Категория": category,
                "Сумма": amount,
                "Описание": description
            }
            self.save_entries()
        except Exception as e:
            print(f"Ошибка при редактировании записи: {e}")

    def search_entries(self, category: Optional[str] = None,
                       date: Optional[datetime.datetime] = None,
                       amount: Optional[float] = None) -> List[Dict[str, str]]:
        """
        Выполняет поиск финансовых записей по заданным критериям.

        Параметры:
            - category: Optional[str]: Категория, по которой осуществляется поиск.
            - date: Optional[datetime.datetime]: Дата, по которой осуществляется поиск.
            - amount: Optional[float]: Сумма, по которой осуществляется поиск.

        Возвращает:
            - List[Dict[str, str]]: Список найденных записей.
        """
        results = []
        for entry in self.entries:
            if (not category or entry['Категория'] == category) and \
               (not date or entry['Дата'] == date.strftime("%Y-%m-%d")) and \
               (amount is None or float(entry['Сумма']) == amount):
                results.append(entry)
        return results

    def show_balance(self) -> Tuple[float, float, float]:
        """
        Отображает текущий баланс, сумму доходов и расходов.

        Возвращает:
            - Tuple[float, float, float]: Кортеж, содержащий сумму доходов, сумму расходов и текущий баланс.
        """
        total_income = sum(float(entry['Сумма']) for entry in self.entries if entry['Категория'] == 'Доход')
        total_expense = sum(float(entry['Сумма']) for entry in self.entries if entry['Категория'] == 'Расход')
        total_balance = total_income - total_expense
        print('=================================')
        print(f"| Текущий баланс: {total_balance}\t\t|")
        print(f"| Доходы: {total_income}\t\t\t\t|")
        print(f"| Расходы: {total_expense}\t\t\t\t|")
        print('=================================')
        return total_income, total_expense, total_balance


if __name__ == "__main__":
    path = 'wallet.json'

    if os.path.exists(path):
        os.remove(path)

    wallet = FinanceTracker(path)

    wallet.add_entry(datetime.datetime.strptime('2020-10-05', "%Y-%m-%d"),
                     'Доход',
                     60000,
                     'Зарплата')
    wallet.add_entry(datetime.datetime.strptime('2020-10-07', "%Y-%m-%d"),
                     'Расход',
                     3500,
                     'Продукты на неделю')
    wallet.add_entry(datetime.datetime.strptime('2020-10-10', "%Y-%m-%d"),
                     'Расход',
                     3000,
                     'Коммуналка')
    wallet.add_entry(datetime.datetime.strptime('2020-10-12', "%Y-%m-%d"),
                     'Доход',
                     5000,
                     'Премия')
    wallet.edit_entry(0,
                      datetime.datetime.strptime('2020-10-05', "%Y-%m-%d"),
                      'Доход',
                      70000,
                      'Зарплата')

    wallet.show_balance()
