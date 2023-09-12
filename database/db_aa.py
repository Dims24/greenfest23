import psycopg2
from contextlib import closing
from psycopg2.extras import DictCursor
from datetime import datetime


class Data:

    def __init__(self, user_data):
        self.user_data = user_data
        self.conn = self.getConn()
        self.cursor = self.getCursor()

    def getConn(self):
        conn = psycopg2.connect(
            dbname='aa-bot',
            user='aa-bot',
            password='aa-bot',
            host='localhost',
            port='5000'
        )

        return conn

    def getCursor(self):
        cursor = self.conn.cursor()
        return cursor

    def create(self):
        check = f'select exists(SELECT user_id FROM users WHERE user_id = \'{self.user_data.id}\')'
        self.cursor.execute(check)
        result = self.cursor.fetchone()
        if (result[0] == False):
            current_date_time = datetime.now()
            sql_user = "INSERT INTO users (user_id, name, username, created_at) VALUES (%s, %s, %s, %s)"
            values_user = (self.user_data.id, self.user_data.first_name, self.user_data.username, current_date_time)
            self.cursor.execute(sql_user, values_user)
            sql_task = "INSERT INTO tasks (user_id) VALUES (%s)"
            values_tasks = (self.user_data.id,)
            self.cursor.execute(sql_task, values_tasks)
            sql_answer_tent = "INSERT INTO tent_answer (user_id) VALUES (%s)"
            values_answer_tent = (self.user_data.id,)
            self.cursor.execute(sql_answer_tent, values_answer_tent)
            sql_furniture_answer = "INSERT INTO furniture_answer (user_id) VALUES (%s)"
            values_answer_furniture = (self.user_data.id,)
            self.cursor.execute(sql_furniture_answer, values_answer_furniture)
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def table(self):
        dict_cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute('SELECT * FROM tasks WHERE user_id = \'{}\''.format(self.user_data.id))
        rec = dict_cur.fetchone()

        return rec

    def response_answer(self, table_name, column_name):
        dict_cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute(f'SELECT {column_name} FROM {table_name} WHERE user_id = \'{self.user_data.id}\'')
        rec = dict_cur.fetchone()

        return rec

    def replace(self, column_name):
        self.cursor.execute(f'UPDATE tasks SET {column_name} = true WHERE user_id = \'{self.user_data.id}\'')
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def replace_answer(self, table_name, column_name):
        self.cursor.execute(f'UPDATE {table_name} SET {column_name} = true WHERE user_id = \'{self.user_data.id}\'')
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def check(self, column_name):
        self.cursor.execute(f'SELECT {column_name} FROM tasks WHERE user_id = \'{self.user_data.id}\'')
        rec = self.cursor.fetchone()
        self.cursor.close()
        self.conn.close()
        return rec[0]

    def check_final(self):
        dict_cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute(f'SELECT antiquiz, tents, furniture, casino FROM tasks WHERE user_id = \'{self.user_data.id}\'')
        rec = dict_cur.fetchone()
        self.cursor.close()
        self.conn.close()
        return rec

    def check_answer_final(self, table_name):
        dict_cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute(f'SELECT answer_1, answer_2, answer_3, answer_4,answer_5 FROM {table_name} WHERE user_id = \'{self.user_data.id}\'')
        rec = dict_cur.fetchone()
        self.cursor.close()
        self.conn.close()
        return rec

    def collection(self, name_input, username=None):
        if username == None:
            update_query = "update users set name = %s where user_id = %s"
            self.cursor.execute(update_query, (name_input, str(self.user_data.id)))
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        else:
            try:
                update_query = "update users set name = %s, username = %s where user_id = %s"
                self.cursor.execute(update_query, (name_input, username, str(self.user_data.id)))
                self.conn.commit()
                self.cursor.close()
                self.conn.close()
            except Exception as error:
                print(error)

    def collection_phone(self, phone):
        update_query = "update users set number = %s where user_id = %s"
        self.cursor.execute(update_query, (phone, str(self.user_data.id)))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def flag_change(self):
        update_query = f'UPDATE collector SET flag = \'win\' where user_id = {self.user_id}'
        self.cursor.execute(update_query)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def check_user_collector(self):
        check = f'select exists(SELECT user_id FROM users WHERE user_id = \'{self.user_data.id}\')'
        self.cursor.execute(check)
        result = self.cursor.fetchone()
        return result[0]
