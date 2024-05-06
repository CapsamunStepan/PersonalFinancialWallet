from tracker import FinanceTracker
import datetime


def main():
    file_path = "finances.json"
    tracker = FinanceTracker(file_path)
    while True:
        print("\n1. Вывод баланса")
        print("2. Добавление записи")
        print("3. Редактирование записи")
        print("4. Поиск по записям")
        print("5. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            tracker.show_balance()
        elif choice == "2":
            try:
                date = datetime.datetime.strptime(input("Введите дату (гггг-мм-дд): "), "%Y-%m-%d")
                category = input("Введите категорию (Доход/Расход): ")
                amount = float(input("Введите сумму: "))
                description = input("Введите описание: ")
                tracker.add_entry(date, category, amount, description)
            except ValueError as VE:
                print(VE)
        elif choice == "3":
            try:
                index = int(input("Введите номер записи для редактирования: "))
                if index not in range(0, len(tracker.entries)):
                    print("Введен неправильный индекс")
                else:
                    try:
                        date = datetime.datetime.strptime(input("Введите новую дату (гггг-мм-дд): "), "%Y-%m-%d")
                        category = input("Введите новую категорию (Доход/Расход): ")
                        amount = float(input("Введите новую сумму: "))
                        description = input("Введите новое описание: ")
                        tracker.edit_entry(index, date, category, amount, description)
                    except ValueError as VE:
                        print(VE)
            except ValueError as VE:
                print(VE)

        elif choice == "4":
            category = input("Введите категорию для поиска или оставьте пустым: ")
            date_str = input("Введите дату для поиска (гггг-мм-дд) или оставьте пустым: ")
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d") if date_str else None
            amount_input = input("Введите сумму для поиска или оставьте пустым: ")
            amount = float(amount_input) if amount_input else None

            results = tracker.search_entries(category, date, amount)
            if results:
                print("\nРезультаты поиска:")
                for result in results:
                    print(result)
            else:
                print("\nНичего не найдено.")
        elif choice == "5":
            print("До свидания!")
            break
        else:
            print("Некорректный ввод. Пожалуйста, выберите действие из списка.")


if __name__ == "__main__":
    main()
