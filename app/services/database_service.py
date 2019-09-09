import psycopg2 as pg
import configparser as cp
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
c = cp.ConfigParser()

c.read(dir_path + '/../conf/config.ini')


def connect():
    try:
        connection = pg.connect(user=c['postgresqlDB']['user'],
                                password=c['postgresqlDB']['pass'],
                                host=c['postgresqlDB']['host'],
                                port="5432",
                                database=c['postgresqlDB']['db'])
        print("You are connected!")
        return connection
    except (Exception, pg.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    # finally:
    #    if connection:
    #        connection.close()
    #        print("PostgreSQL connection is closed")


def set_columns(data, cur):
    items = []
    if data:
        for x in data:
            item = {}
            c = 0
            for col in cur.description:
                item.update({col[0]: x[c]})
                c = c + 1
            items.append(item)
        return items
    else:
        return []


def run_get_query(cur, query, params):
    try:
        if params:
            cur.execute(query, tuple(params))
        else:
            cur.execute(query)
        records = cur.fetchall()
        return {"status": True, "message": "", "data": records}
    except pg.InternalError as e:
        return {"status": False, "message": str(e), "data": None}


def run_upsert_query(conn, q, params):
    try:
        cur = conn.cursor()
        cur.execute(q, tuple(params))
        conn.commit()

        id = cur.fetchone()[0]
        return {"status": True, "message": "", "data": id}
    except pg.InternalError as e:
        conn.rollback()
        return {"status": False, "message": str(e), "data": None}


def run_delete_query(conn, q, params):
    try:
        cur = conn.cursor()
        cur.execute(q, tuple(params))
        conn.commit()
        return {"status": True, "message": "", "data": None}
    except pg.InternalError as e:
        conn.rollback()
        return {"status": False, "message": str(e), "data": None}
