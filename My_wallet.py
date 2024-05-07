import csv
import pandas as pd

from datetime import date


def control_func() -> None:
    """
    Управляющая функция, реализует выбор действий пользователя
    :return: None
    """
    control_dict = {
        1: create_record,
        2: change_record,
        3: read_find_record,
        4: read_record,
        5: read_balance,
        6: False,
    }
    while True:
        print("\nМеню для управления кошельком. Выберите желаемое действие")
        user_val = input("1 - создать запись\n2 - изменить запись\n3 - найти запись\n"
                         "4 - вывести список всех записей\n5 - показать баланс\n6 - выйти из программы\n")
        try:
            control_dict.get(int(user_val))()
        except:
            break


def read_balance() -> None:
    """
    Выводим состояние баланса. Баланс может быть отрицательным,
    так как в условиях не указано обратное
    :return: None
    """
    try:
        with open("data.csv", mode='r', encoding="windows-1251") as reader_file:
            reader_data = csv.reader(reader_file, delimiter=";")
            pozitiv_balance = 0
            negativ_balance = 0
            for row in reader_data:
                if row[1] == 'Доход':
                    pozitiv_balance += int(row[2])      # считаем сумму доходов всего
                else:
                    negativ_balance += int(row[2])      # считаем сумму расходов всего
            balance = pozitiv_balance - negativ_balance     # сводим дебет с кредитом
    finally:
        print(f"Ваш баланс составляет: {balance}\nДоходы - {pozitiv_balance}\nРасходы - {negativ_balance}")



def read_record() -> None:
    """
    Выводим список транзакций.
    :return: None
    """
    with open("data.csv", mode='r', encoding="windows-1251") as reader_file:
        reader_data = csv.reader(reader_file, delimiter=";")
        for row in reader_data:
            print(f"Дата: {row[0]}\nКатегория: {row[1]}\nСумма: {row[2]}\nОписание: {row[3]}\n")


def read_find_record() -> None:
    """
    Функция выводит список записей из файла по заданному ключевому слову.
    :return: None
    """
    for i in seeker()[0]:
        print(f"\nДата: {i[0]}\nКатегория: {i[1]}\nСумма: {i[2]}\nОписание: {i[3]}\n")



def create_record() -> None:
    """
    Функция реализует метод для добавления записей в файл
    :return: None
    """
    try:
        # Создание новой записи при помощи модуля Pandas
        simple_dict = []
        time_record = date.today()
        just_dict = {1: 'Расход', 2: 'Доход'}
        category = just_dict[int(input("Введите категорию денежных средств\n1 - Расход\n2 - Доход\n"))]
        money = input("Введите сумму\n")
        descriptions = input("Опишите транзакцию\n")
        simple_dict.append([time_record, category, money, descriptions])
        headers = ['time_record', 'category', 'money', 'descriptions']
        pd.DataFrame(simple_dict, columns=headers). \
            to_csv('data.csv', mode='a', sep=';', encoding='windows-1251', header=False, index=False)
        # pd.DataFrame(just_list, columns=headers).sort_values(by=['time_record'], ascending=True, ignore_index=True, axis=1)
    finally:
        print("Новая запись создана!")


def change_record() -> None:
    """
    Функция реализует метод для изменения записи в файле
    :return: None
    """
    mid_list = []
    middle_val = seeker()    # Присваиваем переменной результат поиска записи и значение, по которому велся поиск
    try:
        for i in middle_val[0]:
            print(f"\nДата: {i[0]}\nКатегория: {i[1]}\nСумма: {i[2]}\nОписание: {i[3]}\n")
        if len(middle_val[0]) > 1:      # Если нашлось более одной записи
            print("Уточните ваш запрос")
            change_record()  # Выбор записи для изменения
        else:
            print("Создайте новую запись")
            create_record()  # Создание новой записи
            with open("data.csv", mode='r', encoding='windows-1251') as reader:  # Отсеиваем ненужную запись
                for row in reader.readlines():
                    if middle_val[1] not in row:
                        mid_list.append(row)
            with open("data.csv", mode='w', encoding="windows-1251") as new_reader:  # Переписываем справочник
                for new_row in mid_list:
                    new_reader.write(new_row)
    finally:
        print("Запись успешно изменена")


def seeker() -> list:
    """
    Функция для поиска записей по запросу пользователя
    :return: list
    """
    rez_list = []
    seek_value = input("Введите значение для поиска\n")
    with open("data.csv", encoding="windows-1251") as reader_file:
        reader_data = csv.reader(reader_file, delimiter=";")
        for row in reader_data:
            if seek_value.capitalize() in row or seek_value in row:  # Отсев по заданному значению
                rez_list.append(row)  # фиксация найденной записи в список
        if len(rez_list) == 0:
            print("Такой записи в справочнике нет")
        else:
            return [rez_list, seek_value]



def exit_program() -> bool:
    """
    Выходим из программы
    :return: bool
    """
    return False


if __name__ == '__main__':
    control_func()
