import datetime
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
yesterday_str = yesterday.strftime('%Y-%m-%d')
current_date =  yesterday_str

import pandas as pd
import psycopg2
import psycopg2.extras


from logger import logging
import traceback
from Error_func  import  errorEmail
try:
    HOST = 'smartfix-fng-rds.ckwtvqflhmbr.ap-south-1.rds.amazonaws.com'
    PORT = 5432
    USER = 'postgres'
    PASSWORD = 'postgres'
    DATABASE = 'smartfix_db'

    logging.info('started  Fetching Data from db')

    def execute_query(query_string, _id=None):
        # execute query on singleton db connection
        print('*********PostgresDBConnection execute_query called*********', query_string)
        connection = None
        try:
            connection = psycopg2.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE)

            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            fetch_all_as_dict = lambda x: [dict(row) for row in x]
            cursor.execute(query_string)
            result = fetch_all_as_dict(cursor)
            cursor.close()
            return result
        except (Exception, psycopg2.Error, psycopg2.DatabaseError) as error:
            print("Error while fetching data from PostgreSQL - ", error)
        finally:
            if (connection) is not None:
                connection.close()
                print("PostgreSQL connection is closed")


    try:
        data = pd.DataFrame(execute_query(
            f"SELECT * FROM machines_sensorvaluesresample WHERE machines_sensorvaluesresample.resample_timestamp BETWEEN '{yesterday_str} 00:00:00.000' AND '{yesterday_str} 23:59:59.000';"))
        data = data.pivot_table(index='resample_timestamp', values='resample_value', columns='sensor_id')
        data.to_csv(f'/home/ubuntu/democron/{yesterday_str}.csv')
    except Exception as e:
        print(e)
    logging.info('Data Fetched from db')
except Exception as e:
    logging.critical('error while fetching data from db...')
    subj = 'Rrror while fetching data from db'
    error = traceback.format_exc()
    errorEmail(error, subj)







