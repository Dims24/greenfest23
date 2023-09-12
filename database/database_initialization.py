import psycopg2


def init_database():
    conn = psycopg2.connect(
        dbname='aa-bot',
        user='aa-bot',
        password='aa-bot',
        host='localhost',
        port='5000'
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()

    cur.execute("SELECT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'users')")
    table_exists = cur.fetchone()[0]

    # Create a table
    if not table_exists:
        init_user = """
                        create table users
                (
                    id SERIAL PRIMARY KEY,
                    user_id varchar not null,
                    name     varchar not null,
                    surname     varchar not null,
                    username varchar,
                    number   varchar,
                    start_at time ,
                    end_at   time NULL
                );
        """
        init_task = """
                        create table tasks
                (
                    id          SERIAL PRIMARY KEY,
                    user_id     varchar not null,
                    air_1    boolean default false,
                    earth_1    boolean default false,
                    fire_1    boolean default false,
                    air_2    boolean default false,
                    water_1    boolean default false,
                    water_2    boolean default false,
                    earth_2    boolean default false,
                    fire_2    boolean default false,
                    earth_3    boolean default false,
                    fire_3       boolean default false
                );
        """
        tent_answer = """
                                create table tent_answer
                        (
                            id          SERIAL PRIMARY KEY,
                            user_id     varchar not null,
                            answer_1    boolean default false,
                            answer_2       boolean default false,
                            answer_3   boolean default false,
                            answer_4      boolean default false,
                            answer_5      boolean default false
                        );
                """
        furniture_answer = """
                                        create table furniture_answer
                                (
                                    id          SERIAL PRIMARY KEY,
                                    user_id     varchar not null,
                                    answer_1    boolean default false,
                                    answer_2       boolean default false,
                                    answer_3   boolean default false,
                                    answer_4      boolean default false,
                                    answer_5      boolean default false
                                );
                        """
        cur.execute(init_user)
        cur.execute(init_task)
        cur.execute(tent_answer)
        cur.execute(furniture_answer)

    # Commit the transaction and close the cursor and connection
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    init_database()
