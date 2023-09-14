import psycopg2


def init_database():
    conn = psycopg2.connect(
        dbname='greenfest-bot',
        user='greenfest-bot',
        password='greenfest-bot',
        host='localhost',
        port='5001')

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
                    name     varchar,
                    surname     varchar,
                    username varchar,
                    number   varchar,
                    start_at time ,
                    end_at   time NULL,
                    delta   time NULL
                );
        """
        init_task = """
                        create table tasks
                (
                    id          SERIAL PRIMARY KEY,
                    user_id     varchar not null,
                    air_1_1    boolean default false,
                    air_1_2    boolean default false,
                    earth_1_1    boolean default false,
                    earth_1_2    boolean default false,
                    fire_1_1    boolean default false,
                    fire_1_2    boolean default false,
                    air_2_1    boolean default false,
                    air_2_2    boolean default false,
                    water_1_1    boolean default false,
                    water_1_2    boolean default false,
                    water_2_1    boolean default false,
                    water_2_2    boolean default false,
                    earth_2_1    boolean default false,
                    earth_2_2    boolean default false,
                    fire_2_1    boolean default false,
                    fire_2_2    boolean default false,
                    earth_3_1    boolean default false,
                    earth_3_2    boolean default false,
                    fire_3_1       boolean default false,
                    fire_3_2       boolean default false
                );
        """
        answer = """
                                create table answer
                        (
                            id          SERIAL PRIMARY KEY,
                            user_id     varchar not null,
                            answer_1    boolean default false,
                            answer_2       boolean default false,
                            answer_3   boolean default false,
                            answer_4      boolean default false
                        );
                """

        answer_sticker = """
                                        create table answer_sticker
                                (
                                    id          SERIAL PRIMARY KEY,
                                    user_id     varchar not null,
                                    answer_1    boolean default false,
                                    answer_2       boolean default false,
                                    answer_3   boolean default false,
                                    answer_4      boolean default false
                                );
                        """
        cur.execute(init_user)
        cur.execute(init_task)
        cur.execute(answer)
        cur.execute(answer_sticker)

    # Commit the transaction and close the cursor and connection
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    init_database()
