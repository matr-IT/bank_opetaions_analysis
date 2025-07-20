import pandas as pd


def load_transactions(file_path: str) -> pd.DataFrame:
    """Читает Excel-файл и выдает DataFrame"""
    try:
        df = pd.read_excel(file_path)
        return df
    except ValueError as ex:
        print(ex)
    except FileNotFoundError as ex:
        print(ex)


def home_page(date_time: str) -> list[dict]:
    """Функция отображает данные по картам: номер, сумму трат по карте и полученный кэшбэк"""
    date_time_pd = pd.to_datetime(date_time)
    operations = load_transactions('/Users/rybin/PycharmProjects/bank_operations_analysis/data/operations.xlsx')
    operations['Дата операции'] = pd.to_datetime(operations['Дата операции'])
    first_day_of_month = date_time_pd.replace(day=1)
    filtered = operations[operations['Дата операции']] >= first_day_of_month
    filtered = filtered[filtered['Дата операции']] <= date_time_pd

    card_data = []
    for card in filtered['Номер карты'].dropna().unique():
        card_transactions = filtered[filtered['Номер карты'] == card]
        total_spent = sum([i for i in card_transactions['Сумма операции'] if i < 0])
        card_data.append({
            "last_digits": card[-4:],
            "total_spent": float(total_spent),
            "cashback": round(float(total_spent * 0.01), 2)
        })
    return card_data

