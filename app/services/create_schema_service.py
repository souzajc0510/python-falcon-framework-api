import psycopg2
import database_service

conn = database_service.connect()


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS athlete (
            athlete_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            phone VARCHAR(255) NOT NULL,
            gender VARCHAR(255) NOT NULL,
            birthday DATE NOT NULL
        )
        """,
        """ CREATE TABLE IF NOT EXISTS plan (
                   plan_id SERIAL PRIMARY KEY,
                   athlete_id INTEGER NOT NULL,
                   name VARCHAR(255) NOT NULL,
                   description TEXT NOT NULL,
                   difficulty VARCHAR(255) NOT NULL,
                        FOREIGN KEY (athlete_id)
                            REFERENCES athlete (athlete_id)
                            ON UPDATE CASCADE ON DELETE CASCADE
               )
        """,
        """
                CREATE TABLE IF NOT EXISTS exercise (
                    exercise_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT NOT NULL
                )
                """
    )

    try:
        cur = conn.cursor()
        for c in commands:
            cur.execute(c)
            print("Table was created successfully!")
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
