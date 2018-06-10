import pandas as pd
import psycopg2
import sql_query
from sql_query import query0, query1

def get_data():
    connection = psycopg2.connect(host="localhost", database="city4age", user="postgres", password="postgres")
    cur = connection.cursor()
    sql = sql_query.query1
    cur.execute(sql)
    df = pd.DataFrame(curr.fetchall())
    print (df)