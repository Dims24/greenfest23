import os

import pandas as pd
import psycopg2
from datetime import date
from telebot.types import InputFile

def export_data():
    conn = psycopg2.connect(
        dbname='greenfest-bot',
        user='greenfest-bot',
        password='greenfest-bot',
        host='localhost',
        port='5001'
    )
    cur = conn.cursor()

    # Fetch the data from the table using a query
    query = 'SELECT id, name, surname, username, number,start_at,end_at,delta FROM users'
    cur.execute(query)
    data = cur.fetchall()

    # Load the data into a pandas DataFrame
    df = pd.DataFrame(data, columns=['№', 'Имя', 'Фамилия', 'Username', 'Телефон', 'Начало', "Конец", "Время выполнения"])
    current_date = date.today()
    # Export the DataFrame to Excel
    df.to_excel(f'{current_date}.xlsx', index=False)
    path = os.path.join(os.getcwd(), f'{current_date}.xlsx')
    return path