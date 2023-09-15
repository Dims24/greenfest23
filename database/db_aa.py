import psycopg2
from contextlib import closing
from psycopg2.extras import DictCursor
import datetime
from datetime import datetime, date, time


class Data:

    def __init__(self, user_data):
        self.user_data = user_data
        self.conn = self.getConn()
        self.cursor = self.getCursor()

    def getConn(self):
        conn = psycopg2.connect(
            dbname='greenfest-bot',
            user='greenfest-bot',
            password='greenfest-bot',
            host='localhost',
            port='5001'
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
            sql_user = "INSERT INTO users (user_id, username) VALUES (%s,  %s)"
            values_user = (self.user_data.id, self.user_data.username)
            self.cursor.execute(sql_user, values_user)
            sql_task = "INSERT INTO tasks (user_id) VALUES (%s)"
            values_tasks = (self.user_data.id,)
            self.cursor.execute(sql_task, values_tasks)
            sql_answer = "INSERT INTO answer (user_id) VALUES (%s)"
            values_answer_tent = (self.user_data.id,)
            self.cursor.execute(sql_answer, values_answer_tent)
            sql_answer_sticker = "INSERT INTO answer_sticker (user_id) VALUES (%s)"
            values_answer_sticker = (self.user_data.id,)
            self.cursor.execute(sql_answer_sticker, values_answer_sticker)
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def setName(self, name):
        update_query = "update users set name = %s where user_id = %s"
        self.cursor.execute(update_query, (name, str(self.user_data.id)))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def setSurname(self, surname):
        update_query = "update users set surname = %s where user_id = %s"
        self.cursor.execute(update_query, (surname, str(self.user_data.id)))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def setPhone(self, number):
        current_date_time = datetime.now()
        update_query = "update users set number = %s, start_at = %s where user_id = %s"
        self.cursor.execute(update_query, (number, current_date_time, str(self.user_data.id)))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def replace(self, column_name):
        self.cursor.execute(f'UPDATE tasks SET {column_name} = true WHERE user_id = \'{self.user_data.id}\'')
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
        dict_cur.execute(
            f'SELECT air_1_1,air_1_2,earth_1_1,earth_1_2,fire_1_1,fire_1_2,air_2_1,air_2_2,water_1_1,water_1_2,water_2_1,water_2_2,earth_2_1,earth_2_2,fire_2_1,fire_2_2,earth_3_1,earth_3_2,fire_3_1,fire_3_2 FROM tasks WHERE user_id = \'{self.user_data.id}\'')
        rec = dict_cur.fetchone()
        dict_cur.close()
        return rec

    def final(self):
        dict_cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        current_date_time = datetime.now()
        delta = self.delta(current_date_time)
        update_query = "update users set end_at = %s, delta = %s where user_id = %s"
        dict_cur.execute(update_query, (current_date_time, delta, str(self.user_data.id)))
        dict_cur.close()
        self.conn.commit()

    def delta(self, end_at):
        dict_cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute(f'SELECT start_at from users where user_id = \'{self.user_data.id}\'')
        rec = dict_cur.fetchone()
        dict_cur.close()
        start_datetime = datetime.combine(date(1970, 1, 1), rec[0])
        end_datetime = datetime.combine(date(1970, 1, 1), end_at.time())

        time_difference = end_datetime - start_datetime

        return time_difference

    def check_answer_final(self, table_name):
        dict_cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute(
            f'SELECT answer_1, answer_2, answer_3, answer_4 FROM {table_name} WHERE user_id = \'{self.user_data.id}\'')
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
