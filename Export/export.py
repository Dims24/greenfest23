import os

import pandas as pd
import psycopg2
from datetime import date
from telebot.types import InputFile

def export_data():
    conn = psycopg2.connect(
        dbname='aa-bot',
        user='aa-bot',
        password='aa-bot',
        host='localhost',
        port='5000'
    )
    cur = conn.cursor()

    # Fetch the data from the table using a query
    query = 'SELECT id, name, username, number,created_at FROM users'
    cur.execute(query)
    data = cur.fetchall()

    # Load the data into a pandas DataFrame
    df = pd.DataFrame(data, columns=['№', 'Имя', 'Username', 'Телефон', 'Дата создания'])
    current_date = date.today()
    # Export the DataFrame to Excel
    df.to_excel(f'{current_date}.xlsx', index=False)
    path = os.path.join(os.getcwd(), f'{current_date}.xlsx')
    return path