import datetime
import json
import requests
import logging



def greeting():
    current_hour = datetime.datetime.now().hour
    """На основе текущего времени функция возвращает приветствие"""
    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"
