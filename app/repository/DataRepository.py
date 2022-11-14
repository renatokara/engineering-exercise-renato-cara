import typing
from flask import current_app
from service.Database import DatabaseSingleton
from model.data import Data
import datetime
import logging
logger = logging.getLogger()

def get_all_data() -> typing.List[Data]:
    """
        Retrieve all data items in the database
    """
    db = DatabaseSingleton().create()
    result = list()
    cur = db.cursor()
    try:
        print(f"cursor {cur=}")
        cur.execute("SELECT id, url, title, date_added FROM data ")
        rv = cur.fetchall()
        for r in rv:
            result.append(get_data_from_cursor(r))
    except Exception as e:
        logger.error(f"Error query {str(e)}")
    finally:
        cur.close()
        db.close()
    return result



def get_data_by_id(id: int) -> Data:
    """
        Retrieve data items in the database by the given id
    """
    db = DatabaseSingleton().create()
    cur = db.cursor()
    result: Data = None
    try:

        cur.execute("SELECT id, url, title, date_added FROM data WHERE id = %s", (id,))
        r = cur.fetchone()
        if r is not None:
            result = get_data_from_cursor(r)

    except Exception as e:
        logger.error(f"Error query {str(e)}")
    finally:
        cur.close()
        db.close()
    return result


def insert_data(data: Data) -> None:
    """
        Insert data in the database
    """
    db = DatabaseSingleton().create()
    cur = db.cursor()
    try:
        print("inserting", (data.id, data.url, data.title, data.date_added))
        cur.execute("INSERT INTO data(url, title, date_added) \
            VALUES (%s, %s, %s)", (data.url, data.title, data.date_added))
        db.commit()

    except Exception as e:
        logger.error("Error inserting data ",e)
        db.rollback()
    finally:
        cur.close()
        db.close()



def update_data(data: Data) -> None:
    """
        Update data in the database
    """
    db = DatabaseSingleton().create()
    cur = db.cursor()
    try:
        cur.execute("UPDATE data set url = %s, title = %s, date_added = %s \
            WHERE id = %s", (data.url, data.title, data.date_added, data.id))
        db.commit()
    except Exception as e:
        logger.error("Error updating data ",e)
        db.rollback()
    finally:
        cur.close()
        db.close()


def delete_data(id: int) -> None:
    """
        Delete the data in the database by the given id
    """
    db = DatabaseSingleton().create()
    try:
        cur = db.cursor()
        cur.execute("DELETE FROM data WHERE id = %s", (id,))
        db.commit()
    except:
        logger.error("Error removing data")
        db.rollback()
    finally:
        db.close()



def get_data_by_filter(title: str, uri: str, date_before: str, date_after: str ) -> typing.List[Data]:
    """
    Filters the data by any given parameter 
        {
            "title": "",
            "uri": "",
            "date_before": "",
            "date_after": "",

        }
        Retrieve data items in the database by the given filters 
        each parameter is optional and if not provided will be ignored 
        on the query.
    """
    
    db = DatabaseSingleton().create()
    cur = db.cursor()
    result = list()
    try:
        cur.execute("""
            SELECT id, url, title, date_added 
            FROM data 
        WHERE (%s IS NULL OR LOWER(title) like LOWER(%s) ) 
        AND (%s IS NULL OR LOWER(url) like LOWER(%s) )
        AND (%s IS NULL OR date_added < %s) 
        AND (%s IS NULL OR date_added > %s)
        """, (title, fmt_like(title), uri, fmt_like(uri), date_before, date_before, date_after, date_after))
        rv = cur.fetchall()
        for r in rv:
            result.append(get_data_from_cursor(r))

    except Exception as e:
        logger.error(f"Error filter {str(e)}")
    finally:
        cur.close()
        db.close()
    return result

def fmt_like(str):
    if str is None:
        return '%%'
    else:
        return f"%{str}%"


def get_data_by_title(title: str) -> typing.List[Data]:
    """
        Retrieve data items in the database by the given title
        May be more than one as title is not unique in Data
    """
    
    db = DatabaseSingleton().create()
    cur = db.cursor()
    result = list()
    try:
        cur.execute("SELECT id, url, title, date_added FROM data WHERE title like %s", (title,))
        rv = cur.fetchall()
        for r in rv:
            result.append(get_data_from_cursor(r))

    except Exception as e:
        logger.error(f"Error query {str(e)}")
    finally:
        cur.close()
        db.close()
    return result



def get_data_by_url(url: str) -> typing.List[Data]:
    """
        Retrieve data items in the database by the given uri (like)
        May be more than one as url is not unique in Data
    """
    
    db = DatabaseSingleton().create()
    cur = db.cursor()
    result: Data = None
    try:
        cur.execute("SELECT id, url, title, date_added FROM data WHERE url like %s", (url,))
        rv = cur.fetchall()
        for r in rv:
            result.append(get_data_from_cursor(r))

    except Exception as e:
        logger.error(f"Error query {str(e)}")
    finally:
        cur.close()
        db.close()
    return result



def get_data_by_date_after(date: datetime) -> typing.List[Data]:
    """
        Retrieve data items in the database that  have a 
        date_added after given date
    """
    
    db = DatabaseSingleton().create()
    cur = db.cursor()
    result: Data = None
    try:
        cur.execute("SELECT id, url, title, date_added FROM data WHERE date_added > %s", (date,))
        rv = cur.fetchall()
        for r in rv:
            result.append(get_data_from_cursor(r))

    except Exception as e:
        logger.error(f"Error query {str(e)}")
    finally:
        cur.close()
        db.close()
    return result


def get_data_by_date_before(date: datetime) -> typing.List[Data]:
    """
        Retrieve data items in the database that  have a 
        date_added before given date
    """
    
    db = DatabaseSingleton().create()
    cur = db.cursor()
    result: Data = None
    try:
        cur.execute("SELECT id, url, title, date_added FROM data WHERE date_added < %s", (date,))
        rv = cur.fetchall()
        for r in rv:
            result.append(get_data_from_cursor(r))

    except Exception as e:
        logger.error(f"Error query {str(e)}")
    finally:
        cur.close()
        db.close()
    return result


def get_data_by_date_between_dates(date_initial: datetime, date_final: datetime) -> typing.List[Data]:
    """
        Retrieve data items in the database that  have a 
        date_added between the two given dates
    """
    
    db = DatabaseSingleton().create()
    cur = db.cursor()
    result: Data = None
    try:
        cur.execute("SELECT id, url, title, date_added FROM data WHERE date_added BETWEEN %s AND %s", (date_initial, date_final))
        rv = cur.fetchall()
        for r in rv:
            result.append(get_data_from_cursor(r))

    except Exception as e:
        logger.error(f"Error query {str(e)}")
    finally:
        cur.close()
        db.close()
    return result

def get_data_from_cursor(r)-> Data :
    """
        Get the Data from resultset assuming the order
        id, url, title, date_added 
    """
    return Data(r[0], r[1], r[2], r[3])